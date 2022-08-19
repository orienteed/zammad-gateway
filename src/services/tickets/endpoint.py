from fastapi import APIRouter, Depends
import os
from pydantic import Json
import requests
from auth.middleware import VerifyTokenRoute
from fastapi.security import HTTPBearer
from db.usersDAO import usersDAO
from models.tickets.model import Ticket
from models.tickets.model import Ticket_update

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get('/search')
def get_tickets(authorization: str = Depends(token_auth_scheme), expand: bool = False, page: int = 1, per_page: int = 8, search: str | None = None, limit: int = 10, sort_by: str | None = None, order_by: str | None = None, filters: Json | None = None):

    username = usersDAO.get_user_data_by_token(authorization.credentials)

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'page': page,
        'per_page': per_page,
        'query': "customer.email:" + username[0],
        'limit': limit,
        'expand': expand
    }

    if search is not None:
        customParams['query'] = customParams['query'] + ", " + search

    if sort_by is not None:
        customParams['sort_by'] = sort_by

    if order_by is not None:
        customParams['order_by'] = order_by

    queryFilters = ""
    queryFilters = createQueryFilters(queryFilters, filters)

    if queryFilters is not "":
        customParams['query'] = customParams['query'] + " AND " + queryFilters

    reply = requests.get('{}/api/v1/tickets/search'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders)

    return reply.json()

def createGroupQueryFilters(queryFilters, filters):
    queryFilters = "group.id:"
    for i in range(len(filters['type'])):
        if i == 0 and len(filters['type']) == 1:
            queryFilters = queryFilters + str(filters['type'][i])
        elif i == 0 and len(filters['type']) > 1:
            queryFilters = queryFilters + "(" + str(filters['type'][i]) + " OR "
        elif i != 0 and i != len(filters['type']) - 1:
            queryFilters = queryFilters + str(filters['type'][i]) + " OR "
        elif i != 0 and i == len(filters['type']) - 1:
            queryFilters = queryFilters + str(filters['type'][i]) + ")"

    return queryFilters


def createStateQueryFilters(queryFilters, filters):
    queryFilters = "state.id:"
    for i in range(len(filters['status'])):
        if i == 0 and len(filters['status']) == 1:
            queryFilters = queryFilters + str(filters['status'][i])
        elif i == 0 and len(filters['status']) > 1:
            queryFilters = queryFilters + "(" + str(filters['status'][i]) + " OR "
        elif i != 0 and i != len(filters['status']) - 1:
            queryFilters = queryFilters + str(filters['status'][i]) + " OR "
        elif i != 0 and i == len(filters['status']) - 1:
            queryFilters = queryFilters + str(filters['status'][i]) + ")"

    return queryFilters


def createQueryFilters(queryFilters, filters):
    if len(filters['status']) != 0 and len(filters['type']) != 0:
        queryFilters = createGroupQueryFilters(queryFilters, filters)

        queryFilters = queryFilters + " AND "
        queryFilters = queryFilters + "state.id:"
        
        queryFilters = createStateQueryFilters(queryFilters, filters)

    elif len(filters['type']) != 0 and len(filters['status']) == 0:
        queryFilters = createGroupQueryFilters(queryFilters, filters)            

    elif len(filters['status']) != 0 and len(filters['type']) == 0:
        queryFilters = createStateQueryFilters(queryFilters, filters)

    return queryFilters



@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, authorization: str = Depends(token_auth_scheme), expand: bool = False):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': expand
    }

    reply = requests.get('{}/api/v1/tickets/{}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), ticket_id), params=customParams, headers=customHeaders)

    return reply.json()


@router.post('/')
def create_ticket(ticket: Ticket, authorization: str = Depends(token_auth_scheme), expand: bool = False):
    username = usersDAO.get_user_data_by_token(authorization.credentials)

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json',
        'X-On-Behalf-Of': username[0]
    }

    customBody = {
        "title": ticket.title,
        "group": ticket.group,
        "customer": username[0],
        "article": ticket.article.dict()
    }

    customBody['article']['type'] = "chat"
    customBody['article']['internal'] = False
    customBody['article']['sender'] = "Customer"

    if ticket.article.attachments is not None:
        attachments = []
        count = 0
        for attachment in ticket.article.attachments:
            attachments.append(attachment.dict())
            attachments[count]['mime-type'] = attachments[count].pop(
                'mime_type')
            count += 1

        customBody["article"]["attachments"] = attachments

    customParams = {
        'expand': expand
    }

    reply = requests.post('{}/api/v1/tickets'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders, json=customBody)

    return reply.json()


@router.put("/{ticketId}")
def update_ticket(ticketId: int, ticket_update: Ticket_update, authorization: str = Depends(token_auth_scheme), expand: bool = False):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customBody = {
        "state": ticket_update.state.replace('_', ' ')
    }

    customParams = {
        'expand': expand
    }

    reply = requests.put('{0}/api/v1/tickets/{1}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), ticketId), params=customParams, headers=customHeaders, json=customBody)

    return reply.json()
