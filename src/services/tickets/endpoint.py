from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from models.tickets.model import Ticket
from models.tickets.model import Ticket_update
from pydantic import Json
import os
import requests
from logs.setup import logger
from datetime import datetime

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/search")
def get_tickets(
    authorization: str = Depends(token_auth_scheme),
    expand: bool = False,
    page: int = 1,
    per_page: int = 8,
    search: str | None = None,
    limit: int = 10,
    sort_by: str | None = None,
    order_by: str | None = None,
    filters: Json | None = None,
    request: Request = None,
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
        + " - Fetching tickets..."
    )

    username = usersDAO.get_user_data_by_token(request.headers.get("csr-authorization"))

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"page": page, "per_page": per_page, "query": "customer.email:" + username[0], "limit": limit, "expand": expand}

    if search is not None:
        customParams["query"] = customParams["query"] + ", " + search

    if sort_by is not None:
        customParams["sort_by"] = sort_by

    if order_by is not None:
        customParams["order_by"] = order_by

    queryFilters = createQueryFilters(filters)

    if queryFilters is not None:
        customParams["query"] = customParams["query"] + " AND " + queryFilters

    reply = requests.get("{}/api/v1/tickets/search".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders)

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
        + " - Tickets fetched"
    )

    return reply.json()


def createGroupQueryFilters(filters):
    return "group.id:({})".format(" OR ".join(map(str, filters["type"])))


def createStateQueryFilters(filters):
    return "state.id:({})".format(" OR ".join(map(str, filters["status"])))


def createQueryFilters(filters):
    if len(filters["status"]) != 0 and len(filters["type"]) != 0:
        return createGroupQueryFilters(filters) + " AND " + createStateQueryFilters(filters)

    elif len(filters["type"]) != 0 and len(filters["status"]) == 0:
        return createGroupQueryFilters(filters)

    elif len(filters["status"]) != 0 and len(filters["type"]) == 0:
        return createStateQueryFilters(filters)


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, request: Request, authorization: str = Depends(token_auth_scheme), expand: bool = False):

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
        + " - Fetching ticket..."
    )

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": expand}

    reply = requests.get(
        "{}/api/v1/tickets/{}".format(os.getenv("ZAMMAD_URL_DOCKER"), ticket_id), params=customParams, headers=customHeaders
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
        + " - Ticket fetched"
    )

    return reply.json()


@router.post("/")
def create_ticket(ticket: Ticket, request: Request, authorization: str = Depends(token_auth_scheme), expand: bool = False):

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
        + " - Creating ticket..."
    )

    username = usersDAO.get_user_data_by_token(request.headers.get("csr-authorization"))

    customHeaders = {
        "Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")),
        "Content-Type": "application/json",
        "X-On-Behalf-Of": username[0],
    }

    customBody = {"title": ticket.title, "group": ticket.group, "customer": username[0], "article": ticket.article.dict()}

    customBody["article"]["type"] = "chat"
    customBody["article"]["internal"] = False
    customBody["article"]["sender"] = "Customer"

    if ticket.article.attachments is not None:
        attachments = []
        count = 0
        for attachment in ticket.article.attachments:
            attachments.append(attachment.dict())
            attachments[count]["mime-type"] = attachments[count].pop("mime_type")
            count += 1

        customBody["article"]["attachments"] = attachments

    customParams = {"expand": expand}

    reply = requests.post(
        "{}/api/v1/tickets".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders, json=customBody
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
        + " - Ticket created"
    )

    return reply.json()


@router.put("/{ticketId}")
def update_ticket(
    ticketId: int, ticket_update: Ticket_update, request: Request, authorization: str = Depends(token_auth_scheme), expand: bool = False
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
        + " - Updating ticket..."
    )

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customBody = {"state": ticket_update.state.replace("_", " ")}

    customParams = {"expand": expand}

    reply = requests.put(
        "{0}/api/v1/tickets/{1}".format(os.getenv("ZAMMAD_URL_DOCKER"), ticketId),
        params=customParams,
        headers=customHeaders,
        json=customBody,
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
        + " - Ticket updated"
    )

    return reply.json()
