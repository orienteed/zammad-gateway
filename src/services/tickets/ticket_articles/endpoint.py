from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from logs.setup import logger
from models.tickets.ticket_articles.model import TicketComment
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/by_ticket/{ticket_id}")
def get_ticket_comments(ticket_id: int, request: Request, authorization: str = Depends(token_auth_scheme), expand: bool = False):

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
        + " - Fetching ticket comments..."
    )

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": expand}

    reply = requests.get(
        "{0}/api/v1/ticket_articles/by_ticket/{1}".format(os.getenv("ZAMMAD_URL_DOCKER"), ticket_id),
        params=customParams,
        headers=customHeaders,
    )

    external_articles = []

    for article in reply.json():
        if article["internal"] is False:
            external_articles.append(article)

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
        + " - Ticket comments fetched "
    )

    return external_articles


@router.post("/")
def send_comment(
    ticket_comment: TicketComment, authorization: str = Depends(token_auth_scheme), expand: bool = False, request: Request = None
):

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
        + " - Sending comment..."
    )

    username = usersDAO.get_user_data_by_token(request.headers.get("api-authorization"))

    customHeaders = {
        "Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")),
        "Content-Type": "application/json",
        "X-On-Behalf-Of": username[0],
    }

    customParams = {"expand": expand}

    customBody = {
        "ticket_id": ticket_comment.ticket_id,
        "body": ticket_comment.body,
        "content_type": ticket_comment.content_type,
        "type": "chat",
        "internal": False,
        "sender": "Customer",
    }

    if ticket_comment.attachments is not None:
        attachments = []
        count = 0
        for attachment in ticket_comment.attachments:
            attachments.append(attachment.dict())
            attachments[count]["mime-type"] = attachments[count].pop("mime_type")
            count += 1

        customBody["attachments"] = attachments

    if not ticket_comment.ticket_closed:
        reply = requests.post(
            "{}/api/v1/ticket_articles".format(os.getenv("ZAMMAD_URL_DOCKER")), headers=customHeaders, params=customParams, json=customBody
        )
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
            + " - Comment sent"
        )
    else:
        response = JSONResponse({"message": "Reopen the ticket to send a new message"})
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
            + " - Reopen the ticket to send a new message"
        )
        return response

    return reply.json()
