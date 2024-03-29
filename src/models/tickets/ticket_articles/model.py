from pydantic import BaseModel
from typing import List


class TicketAttachment(BaseModel):
    filename: str
    data: str
    mime_type: str


class TicketComment(BaseModel):
    ticket_id: int
    ticket_closed: bool
    body: str
    content_type: str
    attachments: List[TicketAttachment]
