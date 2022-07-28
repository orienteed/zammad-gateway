from enum import Enum
from .tickets_states.model import State
from pydantic import BaseModel
from typing import List, Optional

class TicketAttachment(BaseModel):
    filename: str
    data: str
    mime_type: str

class Article(BaseModel):
    subject: str
    body: str
    # type: str
    attachments: Optional[List[TicketAttachment]] = None


class Group(str, Enum):
    ENHANCEMENT: str = "Enhancement"
    ORDER_ISSUE: str = "Order issue"
    SUPPORT_ISSUE:str = "Support issue"


class Ticket(BaseModel):
    title: str
    group: Group = ""
    article: Article


class Ticket_update(BaseModel):
    state: State = ""