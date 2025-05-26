from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
from chessEngine import run_engine, re_instantiate_engines
from utils.logger import log
import time

def get_total_engine_output(request_lines):
    input_lines = get_input_lines(request_lines)
    if input_lines is None:
        return "fullErr"

    engine_outputs = []
    for i, input_line in enumerate(input_lines):
        try:
            start_time = time.time()
            engine_outputs.append(run_engine(input_line))
            log(f"#{i} Engine execution time: {time.time() - start_time}")
        except ChessEngineException as e:
            log(f"ChessEngineException: {e}")
            for j in range(i, len(input_lines)):
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

def get_input_lines(request_lines):
    for i, line in enumerate(request_lines):
        if line == '':
            return request_lines[i + 1:]