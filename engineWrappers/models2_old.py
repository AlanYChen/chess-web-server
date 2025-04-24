import subprocess
from typing import Any, List, Optional
import copy
from os import path
from dataclasses import dataclass
from enum import Enum
import re

from engineWrappers.chessRelatedExceptions import ChessEngineException

class Maia:
    """Integrates the Maia chess engine with Python."""

    _del_counter = 0
    # Used in test_models: will count how many times the del function is called.

    def __init__(
        self, leela_path: str, weights_path:str, parameters: dict = None
    ) -> None:
        self._DEFAULT_PARAMS = {
            "Debug Log File": "",
            "Contempt": 0,
            "Min Split Depth": 0,
            "Threads": 1,
            "Ponder": "false",
            "Hash": 16,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
        }
        self._process = subprocess.Popen(
            [leela_path, "--weights=" + weights_path],
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self._has_quit_command_been_sent = False

        self._put("uci")

        self.info: str = ""

        self._parameters: dict = {}
        self.update_engine_parameters(self._DEFAULT_PARAMS)
        self.update_engine_parameters(parameters)

        self._prepare_for_new_position(True)

    def get_parameters(self) -> dict:
        """Returns current board position.

        Returns:
            Dictionary of current Maia engine's parameters.
        """
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

        if ("Skill Level" in new_param_values) != (
            "UCI_Elo" in new_param_values
        ) and "UCI_LimitStrength" not in new_param_values:
            # This means the user wants to update the Skill Level or UCI_Elo (only one,
            # not both), and that they didn't specify a new value for UCI_LimitStrength.
            # So, update UCI_LimitStrength, in case it's not the right value currently.
            if "Skill Level" in new_param_values:
                new_param_values.update({"UCI_LimitStrength": "false"})
            elif "UCI_Elo" in new_param_values:
                new_param_values.update({"UCI_LimitStrength": "true"})

        if "Threads" in new_param_values:
            # Recommended to set the hash param after threads.
            threads_value = new_param_values["Threads"]
            del new_param_values["Threads"]
            hash_value = None
            if "Hash" in new_param_values:
                hash_value = new_param_values["Hash"]
                del new_param_values["Hash"]
            else:
                hash_value = self._parameters["Hash"]
            new_param_values["Threads"] = threads_value
            new_param_values["Hash"] = hash_value

        for name, value in new_param_values.items():
            self._set_option(name, value, True)
        self.set_fen_position(self.get_fen_position(), False)
        # Getting SF to set the position again, since UCI option(s) have been updated.

    def reset_engine_parameters(self) -> None:
        """Resets the stockfish parameters.

        Returns:
            None
        """
        self.update_engine_parameters(self._DEFAULT_PARAMS)

    def _prepare_for_new_position(self, send_ucinewgame_token: bool = True) -> None:
        if send_ucinewgame_token:
            self._put("ucinewgame")
        self._is_ready()
        self.info = ""

    def _put(self, command: str) -> None:
        if not self._process.stdin:
            raise BrokenPipeError()
        if self._process.poll() is None and not self._has_quit_command_been_sent:
            self._process.stdin.write(f"{command}\n")
            self._process.stdin.flush()
            if command == "quit":
                self._has_quit_command_been_sent = True

    def _read_line(self) -> str:
        if not self._process.stdout:
            raise BrokenPipeError()
        if self._process.poll() is not None:
            raise ChessEngineException("Maia process crashed")
        return self._process.stdout.readline().strip()

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

    def _go_remaining_time(self, wtime: Optional[int], btime: Optional[int]) -> None:
        cmd = "go"
        if wtime is not None:
            cmd += f" wtime {wtime}"
        if btime is not None:
            cmd += f" btime {btime}"
        self._put(cmd)

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

    def set_position(self, moves: Optional[List[str]] = None) -> None:
        """Sets current board position.

        Args:
            moves:
              A list of moves to set this position on the board.
              Must be in full algebraic notation.
              example: ['e2e4', 'e7e5']
        """
        self.set_fen_position(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True
        )
        self.make_moves_from_current_position(moves)

    def make_moves_from_current_position(self, moves: Optional[List[str]]) -> None:
        """Sets a new position by playing the moves from the current position.

        Args:
            moves:
              A list of moves to play in the current position, in order to reach a new position.
              Must be in full algebraic notation.
              Example: ["g4d7", "a8b8", "f1d1"]
        """
        if not moves:
            return
        self._prepare_for_new_position(False)
        for move in moves:
            if not self.is_move_correct(move):
                raise ValueError(f"Cannot make move: {move}")
            self._put(f"position fen {self.get_fen_position()} moves {move}")

    def get_board_visual(self, perspective_white: bool = True) -> str:
        """Returns a visual representation of the current board position.

        Args:
            perspective_white:
              A bool that indicates whether the board should be displayed from the
              perspective of white (True: white, False: black)

        Returns:
            String of visual representation of the chessboard with its pieces in current position.
        """
        self._put("d")
        board_rep_lines = []
        count_lines = 0
        while count_lines < 17:
            board_str = self._read_line()
            if "+" in board_str or "|" in board_str:
                count_lines += 1
                if perspective_white:
                    board_rep_lines.append(f"{board_str}")
                else:
                    # If the board is to be shown from black's point of view, all lines are
                    # inverted horizontally and at the end the order of the lines is reversed.
                    board_part = board_str[:33]
                    # To keep the displayed numbers on the right side,
                    # only the string representing the board is flipped.
                    number_part = board_str[33:] if len(board_str) > 33 else ""
                    board_rep_lines.append(f"{board_part[::-1]}{number_part}")
        if not perspective_white:
            board_rep_lines = board_rep_lines[::-1]
        board_str = self._read_line()
        if "a   b   c" in board_str:
            # Engine being used is recent enough to have coordinates, so add them:
            if perspective_white:
                board_rep_lines.append(f"  {board_str}")
            else:
                board_rep_lines.append(f"  {board_str[::-1]}")
        while "Checkers" not in self._read_line():
            # Gets rid of the remaining lines in _process.stdout.
            # "Checkers" is in the last line outputted by Maia for the "d" command.
            pass
        board_rep = "\n".join(board_rep_lines) + "\n"
        return board_rep

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

    def set_skill_level(self, skill_level: int = 20) -> None:
        """Sets current skill level of stockfish engine.

        Args:
            skill_level:
              Skill Level option between 0 (weakest level) and 20 (full strength)

        Returns:
            None
        """
        self.update_engine_parameters(
            {"UCI_LimitStrength": "false", "Skill Level": skill_level}
        )

    def set_elo_rating(self, elo_rating: int = 1350) -> None:
        """Sets current elo rating of stockfish engine, ignoring skill level.

        Args:
            elo_rating: Aim for an engine strength of the given Elo

        Returns:
            None
        """
        self.update_engine_parameters(
            {"UCI_LimitStrength": "true", "UCI_Elo": elo_rating}
        )

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

    @dataclass
    class BenchmarkParameters:
        ttSize: int = 16
        threads: int = 1
        limit: int = 13
        fenFile: str = "default"
        limitType: str = "depth"
        evalType: str = "mixed"

        def __post_init__(self):
            self.ttSize = self.ttSize if self.ttSize in range(1, 128001) else 16
            self.threads = self.threads if self.threads in range(1, 513) else 1
            self.limit = self.limit if self.limit in range(1, 10001) else 13
            self.fenFile = (
                self.fenFile
                if self.fenFile.endswith(".fen") and path.isfile(self.fenFile)
                else "default"
            )
            self.limitType = (
                self.limitType
                if self.limitType in ["depth", "perft", "nodes", "movetime"]
                else "depth"
            )
            self.evalType = (
                self.evalType
                if self.evalType in ["mixed", "classical", "NNUE"]
                else "mixed"
            )

    def benchmark(self, params: BenchmarkParameters) -> str:
        """Benchmark will run the bench command with BenchmarkParameters.
        It is an Additional custom non-UCI command, mainly for debugging.
        Do not use this command during a search!
        """
        if type(params) != self.BenchmarkParameters:
            params = self.BenchmarkParameters()

        self._put(
            f"bench {params.ttSize} {params.threads} {params.limit} {params.fenFile} {params.limitType} {params.evalType}"
        )
        while True:
            text = self._read_line()
            splitted_text = text.split(" ")
            if splitted_text[0] == "Nodes/second":
                return text

    def set_depth(self, depth_value: int = 2) -> None:
        """Sets current depth of stockfish engine.

        Args:
            depth_value: Depth option higher than 1
        """
        self.depth = str(depth_value)

    class Piece(Enum):
        WHITE_PAWN = "P"
        BLACK_PAWN = "p"
        WHITE_KNIGHT = "N"
        BLACK_KNIGHT = "n"
        WHITE_BISHOP = "B"
        BLACK_BISHOP = "b"
        WHITE_ROOK = "R"
        BLACK_ROOK = "r"
        WHITE_QUEEN = "Q"
        BLACK_QUEEN = "q"
        WHITE_KING = "K"
        BLACK_KING = "k"

    def get_what_is_on_square(self, square: str) -> Optional[Piece]:
        """Returns what is on the specified square.

        Args:
            square:
                The coordinate of the square in question. E.g., e4.

        Returns:
            Either one of the 12 enum members in the Piece enum, or the None
            object if the square is empty.
        """

        file_letter = square[0].lower()
        rank_num = int(square[1])
        if (
            len(square) != 2
            or file_letter < "a"
            or file_letter > "h"
            or square[1] < "1"
            or square[1] > "8"
        ):
            raise ValueError(
                "square argument to the get_what_is_on_square function isn't valid."
            )
        rank_visual = self.get_board_visual().splitlines()[17 - 2 * rank_num]
        piece_as_char = rank_visual[2 + (ord(file_letter) - ord("a")) * 4]
        if piece_as_char == " ":
            return None
        else:
            return Maia.Piece(piece_as_char)

    class Capture(Enum):
        DIRECT_CAPTURE = "direct capture"
        EN_PASSANT = "en passant"
        NO_CAPTURE = "no capture"

    def will_move_be_a_capture(self, move_value: str) -> Capture:
        """Returns whether the proposed move will be a direct capture,
           en passant, or not a capture at all.

        Args:
            move_value:
                The proposed move, in the notation that Maia uses.
                E.g., "e2e4", "g1f3", etc.

        Returns one of the following members of the Capture enum:
            DIRECT_CAPTURE if the move will be a direct capture.
            EN_PASSANT if the move is a capture done with en passant.
            NO_CAPTURE if the move does not capture anything.
        """
        if not self.is_move_correct(move_value):
            raise ValueError("The proposed move is not valid in the current position.")
        starting_square_piece = self.get_what_is_on_square(move_value[:2])
        ending_square_piece = self.get_what_is_on_square(move_value[2:4])
        if ending_square_piece != None:
            if self._parameters["UCI_Chess960"] == "false":
                return Maia.Capture.DIRECT_CAPTURE
            else:
                # Check for Chess960 castling:
                castling_pieces = [
                    [Maia.Piece.WHITE_KING, Maia.Piece.WHITE_ROOK],
                    [Maia.Piece.BLACK_KING, Maia.Piece.BLACK_ROOK],
                ]
                if [starting_square_piece, ending_square_piece] in castling_pieces:
                    return Maia.Capture.NO_CAPTURE
                else:
                    return Maia.Capture.DIRECT_CAPTURE
        elif move_value[2:4] == self.get_fen_position().split()[
            3
        ] and starting_square_piece in [
            Maia.Piece.WHITE_PAWN,
            Maia.Piece.BLACK_PAWN,
        ]:
            return Maia.Capture.EN_PASSANT
        else:
            return Maia.Capture.NO_CAPTURE

    def __del__(self) -> None:
        Maia._del_counter += 1
        if self._process.poll() is None:
            self._put("quit")
            while self._process.poll() is None:
                pass
