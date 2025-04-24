
# For when something in the engine itself is at issue
class ChessEngineException(Exception):
    pass

# For when something given as input to the engine is at issue
class ChessEngineImproperInputException(Exception):
    pass
