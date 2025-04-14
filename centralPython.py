from stockfishPython import Stockfish
import platform

system = platform.system

executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
executable_path = ("../bin/" + executable_name)

stockfish = Stockfish(path=executable_path)