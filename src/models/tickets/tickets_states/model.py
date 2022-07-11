from enum import Enum

from pydantic import BaseModel

class State(str, Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"

