from enum import Enum

class State(Enum):
    DONE = 0
    NULL = 1
    UNKNOWN_COMMAND = 2
    INVALID_DATE = 3
    EMPTY_DATE = 4

