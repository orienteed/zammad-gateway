from pydantic import BaseModel, Json
from typing import List


class TicketAttachment(BaseModel):
    filename: str
    data: str
    mime_type: str

class TicketComment(BaseModel):
    ticket_id: int
    body: str
    content_type: str
    type: str
    internal: bool = False
    sender: str = "Customer"
    attachments: List[TicketAttachment]