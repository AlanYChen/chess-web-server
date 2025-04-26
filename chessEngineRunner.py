from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
from chessEngine import run_engine
from logger import log
import time

def get_total_engine_output(request):
    fens = get_fens(request)
    if fens is None:
        return "fullErr"

    engine_outputs = []
    for i, fen in enumerate(fens):
        try:
            start_time = time.time()
            engine_outputs.append(run_engine(fen))
            log(f"#{i} Engine execution time: {time.time() - start_time}")
        except ChessEngineException as e:
            log(f"ChessEngineException: {e}")
            for j in range(i, len(fens)):
                log(f"Append err: {j}")
                engine_outputs.append("err")
            break
        except ChessEngineImproperInputException as e:
            log(f"ChessEngineImproperInputException: {e}")
            engine_outputs.append("err")
        except Exception as e:
            log(f"Exception: {e}")
            engine_outputs.append("err")
    
    total_engine_output = ','.join(engine_outputs)
    return total_engine_output

def get_fens(request):
    lines = request.splitlines()
    for i, line in enumerate(lines):
        if line == '':
            return lines[i + 1:]
    return None