from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
from chessEngine import run_engine
from logger import log

def get_total_engine_output(request):
    fens = get_fens(request)

    engine_outputs = []
    for i, fen in enumerate(fens):
        try:
            engine_outputs.append(run_engine(fen, i))
        except ChessEngineException as e:
            log(f"ChessEngineException: {e}")
            for j in range(i, len(fens)):
                log(f"Append err: {j}")
                engine_outputs.append("err")
            break
        except ChessEngineImproperInputException as e:
            log(f"ChessEngineImproperInputException: {e}")
            engine_outputs.append("err")
    
    total_engine_output = ','.join(engine_outputs)
    return total_engine_output

def get_fens(request):
    lines = request.splitlines()

    for i, line in enumerate(lines):
        if line == '':
            return lines[i + 1:]
    raise ValueError("get_fens received a request with no empty line")