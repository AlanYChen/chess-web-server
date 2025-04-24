import subprocess
from typing import Any, Optional
import copy
from os import path

from engineWrappers.chessRelatedExceptions import ChessEngineException

class Maia:
    """Integrates the Maia chess engine with Python."""

    _del_counter = 0 # Used in test_models: will count how many times the del function is called.

    def __init__(self, leela_path: str, weights_path: str) -> None:
        self._process = subprocess.Popen(
            [leela_path, "--weights=" + weights_path],
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self._has_quit_command_been_sent = False
        self._parameters: dict = {}
        self.info: str = ""

        self._put("uci")
        self._prepare_for_new_position(True)

    def _put(self, command: str) -> None:
        if not self._process.stdin:
            raise BrokenPipeError()
        if self._process.poll() is None and not self._has_quit_command_been_sent:
            self._process.stdin.write(f"{command}\n")
            self._process.stdin.flush()
            if command == "quit":
                self._has_quit_command_been_sent = True

    def _prepare_for_new_position(self, send_ucinewgame_token: bool = True) -> None:
        if send_ucinewgame_token:
            self._put("ucinewgame")
        self._is_ready()
        self.info = ""

    def _read_line(self) -> str:
        if not self._process.stdout:
            raise BrokenPipeError()
        if self._process.poll() is not None:
            raise ChessEngineException("The Maia process has crashed")
        return self._process.stdout.readline().strip()

    def get_parameters(self) -> dict:
        return self._parameters

    def update_engine_parameters(self, new_param_valuesP: Optional[dict]) -> None:
        """Updates the stockfish parameters.

        Args:
            new_param_values:
                Contains (key, value) pairs which will be used to update
                the _parameters dictionary.

        Returns:
            None
        """
        if not new_param_valuesP:
            return

        new_param_values = copy.deepcopy(new_param_valuesP)

        if len(self._parameters) > 0:
            for key in new_param_values:
                if key not in self._parameters:
                    raise ValueError(f"'{key}' is not a key that exists.")

        for name, value in new_param_values.items():
            self._set_option(name, value, True)
        self.set_fen_position(self.get_fen_position(), False)
        # Getting SF to set the position again, since UCI option(s) have been updated.

    def _set_option(
        self, name: str, value: Any, update_parameters_attribute: bool = True
    ) -> None:
        self._put(f"setoption name {name} value {value}")
        if update_parameters_attribute:
            self._parameters.update({name: value})
        self._is_ready()

    def _is_ready(self) -> None:
        self._put("isready")
        while self._read_line() != "readyok":
            pass

    def _go(self) -> None:
        self._put(f"go nodes 1")

    def set_fen_position(
        self, fen_position: str, send_ucinewgame_token: bool = True
    ) -> None:
        """Sets current board position in Forsyth–Edwards notation (FEN).

        Args:
            fen_position:
              FEN string of board position.

            send_ucinewgame_token:
              Whether to send the "ucinewgame" token to the Maia engine.
              The most prominent effect this will have is clearing Maia's transposition table,
              which should be done if the new position is unrelated to the current position.

        Returns:
            None
        """
        self._prepare_for_new_position(send_ucinewgame_token)
        self._put(f"position fen {fen_position}")

    def get_fen_position(self) -> str:
        """Returns current board position in Forsyth–Edwards notation (FEN).

        Returns:
            String with current position in Forsyth–Edwards notation (FEN)
        """
        self._put("d")
        while True:
            text = self._read_line()
            splitted_text = text.split(" ")
            if splitted_text[0] == "Fen:":
                while "Checkers" not in self._read_line():
                    pass
                return " ".join(splitted_text[1:])

    def get_best_move(self) -> Optional[str]:
        """Returns best move with current position on the board.
        wtime and btime arguments influence the search only if provided.

        Returns:
            A string of move in algebraic notation or None, if it's a mate now.
        """
        self._go()
        return self._get_best_move_from_popen_process()

    def _get_best_move_from_popen_process(self) -> Optional[str]:
        # Precondition - a "go" command must have been sent to SF before calling this function.
        # This function needs existing output to read from the SF popen process.
        last_text: str = ""
        while True:
            text = self._read_line()
            splitted_text = text.split(" ")
            if splitted_text[0] == "bestmove":
                self.info = last_text
                return None if splitted_text[1] == "(none)" else splitted_text[1]
            last_text = text

    def __del__(self) -> None:
        Maia._del_counter += 1
        if self._process.poll() is None:
            self._put("quit")
            while self._process.poll() is None:
                pass
