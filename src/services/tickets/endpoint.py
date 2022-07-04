from dotenv import load_dotenv
from fastapi import APIRouter, Header, Body
import os
import requests
from fastapi.requests import Request
from auth.middleware import VerifyTokenRoute

from db.usersDAO import usersDAO

load_dotenv()

router = APIRouter(route_class=VerifyTokenRoute)


# Get a ticket
@router.get('/search')
def getTickets(expand: bool = False, page: int = 1, per_page: int = 8, search: str = "", limit: int = 10,
               Authorization: str | None = Header(default="")):

    username = usersDAO.get_user_data_by_token(Authorization.split(" ")[1])[0]

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': expand,
        'page': page,
        'per_page': per_page,
        'query': username,
        'limit': limit,
    }

    if search is not "":
        customParams['query'] = customParams['query'] + ", " + search

    reply = requests.get('{}/api/v1/tickets/search'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders)

    return reply.json()


# Create a ticket
@router.post('/')
def createTicket(title: str = Body(default=""), group: str = Body(default=""), customer: str = Body(default=""),
                 article: dict = Body(
                     default={"subject": "", "body": "", "type": "", "internal": False, "sender": ""}),
                 Authorization: str | None = Header(default="")):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customBody = {
        "title": title,
        "group": group,
        "customer": customer,
        "article": article
    }

    reply = requests.post('{}/api/v1/tickets'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), headers=customHeaders, json=customBody)

    return reply.json()


# Update a ticket
@router.put("/{ticketId}")
def updateTicket(ticketId: int, state: dict = Body(default={"state": ""}), Authorization: str | None = Header(default="")):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customBody = {
        "state": state['state']
    }

    reply = requests.put('{0}/api/v1/tickets/{1}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), ticketId), headers=customHeaders, json=customBody)

    return reply.json()
