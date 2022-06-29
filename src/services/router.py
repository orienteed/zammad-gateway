from sys import prefix
from fastapi import APIRouter
from .users import endpoint as customer_endpoint
from .tickets import endpoint as ticket_endpoint
from .tickets.ticket_articles import endpoint as ticket_articles_endpoint
from .tickets.ticket_attachment import endpoint as ticket_attachment_endpoint
from .tickets.tickets_states import endpoint as ticket_states_endpoint
from .groups import endpoint as group_endpoint

api_router = APIRouter()

api_router.include_router(customer_endpoint.router, prefix="/api/v1/users")
api_router.include_router(ticket_endpoint.router, prefix="/api/v1/tickets")
api_router.include_router(ticket_articles_endpoint.router, prefix="/api/v1/ticket_articles")
api_router.include_router(ticket_attachment_endpoint.router, prefix="/api/v1/ticket_attachment")
api_router.include_router(group_endpoint.router, prefix="/api/v1/groups")
api_router.include_router(ticket_states_endpoint.router, prefix="/api/v1/ticket_states")