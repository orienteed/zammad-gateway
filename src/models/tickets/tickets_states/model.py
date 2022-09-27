from enum import Enum


class State(str, Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"
