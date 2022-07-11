from fastapi import APIRouter, Response, Depends
import os
import requests
from fastapi.security import HTTPBearer
from auth.middleware import VerifyTokenRoute


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get('/{ticketId}/{articleId}/{attachmentId}')
def get_attachments(ticketId: int, articleId: int, attachmentId: int, authorization: str = Depends(token_auth_scheme)):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    reply = requests.get('{0}/api/v1/ticket_attachment/{1}/{2}/{3}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), ticketId, articleId, attachmentId), headers=customHeaders)

    headers = {
        "media_type": reply.headers['Content-Type'],
        "Content-Disposition": reply.headers['Content-Disposition']
    }

    return Response(content=reply.content, headers=headers)
