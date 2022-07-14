from enum import Enum
from .tickets_states.model import State
from pydantic import BaseModel


class Article(BaseModel):
    subject: str
    body: str
    type: str
    internal: bool = False


class Group(str, Enum):
    ENHANCEMENT: str = "Enhancement"
    ORDER_ISSUE: str = "Order issue"
    SUPPORT_ISSUE:str = "Support issue"


class Ticket(BaseModel):
    title: str
    group: Group = ""
    customer: str = ""
    article: Article


class Ticket_update(BaseModel):
    state: State = ""