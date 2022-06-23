from fastapi import APIRouter, Header, Body
from dotenv import load_dotenv
import requests
import os

load_dotenv()

router = APIRouter()


# Get ticket comments
@router.get('/by_ticket/{ticketId}')
def getTicketThread(ticketId: int, X_On_Behalf_Of: str, internal: bool, Authorization: str | None = Header(default="")):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_ADMIN_API_KEY')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'X-On-Behalf-Of': X_On_Behalf_Of,
        'internal': internal
    }

    reply = requests.get('{0}/api/v1/ticket_articles/by_ticket/{1}'.format(
        os.getenv('ZAMMAD_URL'), ticketId), params=customParams, headers=customHeaders)

    return reply.json()


# Send a comment into a ticket
@router.post('/')
def sendComment(ticket_id: int = Body(default=""), body: str = Body(default=""), content_type: str = Body(default=""),
                type: str = Body(default=""), internal: bool = Body(default=False), sender: str = Body(default=""),
                attachments: list = Body(default=[{"filename": "", "data": "", "mine-type": ""}]), Authorization: str | None = Header(default="")):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_ADMIN_API_KEY'))
    }

    customBody = {
        "ticket_id": ticket_id,
        "body": body,
        "content_type": content_type,
        "type": type,
        "internal": internal,
        "sender": sender
    }

    if attachments[0]["data"] != "":
        customBody["attachments"] = attachments    

    reply = requests.post('{}/api/v1/ticket_articles'.format(
        os.getenv('ZAMMAD_URL')), headers=customHeaders, json=customBody)

    return reply.json()
