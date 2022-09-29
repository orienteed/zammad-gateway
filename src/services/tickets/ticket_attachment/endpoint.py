from fastapi import APIRouter, Response, Depends
import os
import requests
from fastapi.security import HTTPBearer
from auth.middleware import VerifyTokenRoute
from logs.setup import logger
from datetime import datetime
from fastapi.requests import Request


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/{ticketId}/{articleId}/{attachmentId}")
def get_attachments(ticketId: int, articleId: int, attachmentId: int, request: Request, authorization: str = Depends(token_auth_scheme)):

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + " - Fetching attachment..."
    )

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    reply = requests.get(
        "{0}/api/v1/ticket_attachment/{1}/{2}/{3}".format(os.getenv("ZAMMAD_URL_DOCKER"), ticketId, articleId, attachmentId),
        headers=customHeaders,
    )

    headers = {"media_type": reply.headers["Content-Type"], "Content-Disposition": reply.headers["Content-Disposition"]}

    logger.info(
        "INFO    - ["
        + str(datetime.now())
        + "]: "
        + str(request.client.host)
        + ":"
        + str(request.client.port)
        + " - "
        + str(request.method)
        + " - "
        + str(request.url.path)
        + " - Attachment fetched"
    )

    return Response(content=reply.content, headers=headers)
