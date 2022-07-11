import os
import requests
from fastapi.security import HTTPBearer
from models.tickets.ticket_articles.model import TicketComment
from auth.middleware import VerifyTokenRoute
from fastapi import APIRouter, Depends


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get('/by_ticket/{ticket_id}')
def get_ticket_comments(ticket_id: int, authorization: str = Depends(token_auth_scheme), expand: bool = False):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'internal': False,
        'expand': expand
    }

    reply = requests.get('{0}/api/v1/ticket_articles/by_ticket/{1}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), ticket_id), params=customParams, headers=customHeaders)

    return reply.json()


@router.post('/')
def send_comment(ticket_comment: TicketComment, X_On_Behalf_Of: str, authorization: str = Depends(token_auth_scheme), expand: bool = False):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json',
        'X-On-Behalf-Of': X_On_Behalf_Of
    }

    customParams = {
        'expand': expand
    }

    customBody = {
        "ticket_id": ticket_comment.ticket_id,
        "body": ticket_comment.body,
        "content_type": ticket_comment.content_type,
        "type": ticket_comment.type,
        "internal": ticket_comment.internal,
        "sender": ticket_comment.sender
    }

    if ticket_comment.attachments is not None:
        attachments = []
        count = 0
        for attachment in ticket_comment.attachments:
            attachments.append(attachment.dict())
            attachments[count]['mime-type'] = attachments[count].pop('mime_type')
            count += 1
        
        customBody["attachments"] = attachments

    reply = requests.post('{}/api/v1/ticket_articles'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), headers=customHeaders, params=customParams, json=customBody)

    return reply.json()
