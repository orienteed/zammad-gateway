from fastapi import APIRouter
from .users import endpoint as customer_endpoint
from .tickets import endpoint as ticket_endpoint
from .tickets.ticket_articles import endpoint as ticket_articles_endpoint
from .tickets.ticket_attachment import endpoint as ticket_attachment_endpoint

api_router = APIRouter()

api_router.include_router(customer_endpoint.router, prefix="/api/v1/users")
api_router.include_router(ticket_endpoint.router, prefix="/api/v1/tickets")
api_router.include_router(ticket_articles_endpoint.router, prefix="/api/v1/ticket_articles")
api_router.include_router(ticket_attachment_endpoint.router, prefix="/api/v1/ticket_attachment")