from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
from chessEngine import run_engine, re_instantiate_engines
from utils.logger import log
from utils.fen import is_fen_syntax_valid
import time

def get_total_engine_output(request_lines):
    fens = get_fens(request_lines)
    if fens is None:
        return "fullErr"

    engine_outputs = []
    for i, fen in enumerate(fens):
        if not is_fen_syntax_valid(fen):
            log(f"Invalid fen: {fen}")
            engine_outputs.append("err")
            continue

        try:
            start_time = time.time()
            engine_outputs.append(run_engine(fen))
            log(f"#{i} Engine execution time: {time.time() - start_time}")
        except ChessEngineException as e:
            log(f"ChessEngineException: {e}")
            for j in range(i, len(fens)):
                engine_outputs.append("err")
            re_instantiate_engines()
            break
        except ChessEngineImproperInputException as e:
            log(f"ChessEngineImproperInputException: {e}")
            engine_outputs.append("err")
        except Exception as e:
            log(f"Exception: {e}")
            engine_outputs.append("err")
    
    total_engine_output = ','.join(engine_outputs)
    return total_engine_output

def get_fens(request_lines):
    for i, line in enumerate(request_lines):
        if line == '':
            return request_lines[i + 1:]