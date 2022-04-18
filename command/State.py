from enum import Enum

class State(Enum):
    DONE = 0
    NULL = 1
    INVALID_DATE = 2
    EMPTY_DATE = 3
    NEED_HELP = 4
    NEED_HELP_FOR_COMMAND = 5
    NEED_HELP_FOR_UPDATE = 6
    NEED_HELP_FOR_FETCH = 7


