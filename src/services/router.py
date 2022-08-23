from fastapi import APIRouter
from .tickets import endpoint as ticket_endpoint
from .tickets.ticket_articles import endpoint as ticket_articles_endpoint
from .tickets.ticket_attachment import endpoint as ticket_attachment_endpoint
from .tickets.tickets_states import endpoint as ticket_states_endpoint
from .groups import endpoint as group_endpoint
from .auth import endpoint as auth_endpoint
from .priorities import endpoint as priority_endpoint
from .users import endpoint as users_endpoint

api_router = APIRouter()

api_router.include_router(auth_endpoint.router, prefix='/auth', tags=["Authentication"])
api_router.include_router(users_endpoint.router, prefix='/users', tags=["Users"])
api_router.include_router(group_endpoint.router, prefix="/groups", tags=["Groups"])
api_router.include_router(priority_endpoint.router, prefix="/ticket_priorities", tags=["Priorities"])
api_router.include_router(ticket_articles_endpoint.router, prefix="/ticket_articles", tags=["Tickets Articles"])
api_router.include_router(ticket_attachment_endpoint.router, prefix="/ticket_attachment", tags=["Tickets Attachment"])
api_router.include_router(ticket_endpoint.router, prefix="/tickets", tags=["Tickets"])
api_router.include_router(ticket_states_endpoint.router, prefix="/ticket_states", tags=["Tickets States"])