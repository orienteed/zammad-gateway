from email import header
from fastapi import APIRouter, Header, Response
from dotenv import load_dotenv
import requests
import os

load_dotenv()

router = APIRouter()


@router.get('/{ticketId}/{articleId}/{attachmentId}')
def getAttachments(ticketId: int, articleId: int, attachmentId: int, Authorization: str | None = Header(default="")):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_ADMIN_API_KEY')),
        'Content-Type': 'application/json'
    }

    reply = requests.get('{0}/api/v1/ticket_attachment/{1}/{2}/{3}'.format(
        os.getenv('ZAMMAD_URL'), ticketId, articleId, attachmentId), headers=customHeaders)

    # filename = reply.headers['Content-Disposition'].split(";")[1].split('filename=')[1].replace('"',"")

    headers = {
        "media_type": reply.headers['Content-Type'],
        "Content-Disposition": reply.headers['Content-Disposition']
    }

    return Response(content=reply.content, headers=headers)
