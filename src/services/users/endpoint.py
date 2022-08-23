from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from models.users.model import Customer, Customer_update
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


def createCustomer(customer: Customer):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': True
    }

    customBody = {
        "firstname": customer.firstname,
        "lastname": customer.lastname,
        "email": customer.username,
        "login": customer.username,
        "organization": customer.organization,
        "roles": customer.roles
    }

    reply = requests.post('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders, json=customBody)

    return reply.json()


def getCustomer(customer: Customer):
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json',
        'X-On-Behalf-Of': customer.username
    }

    customParams = {
        'expand': True,
    }

    reply = requests.get('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders)

    return reply.json()[0]


@router.put('/')
def modify_customer(authorization: str = Depends(token_auth_scheme), customer: Customer_update = None):
    user_data = usersDAO.get_user_data_by_token(authorization.credentials)
    print(user_data[3])

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': True
    }

    customBody = {
        'firstname': customer.firstname,
        'lastname': customer.lastname,
        'email': customer.username,
        'login': customer.username
    }

    reply = requests.put('{0}/api/v1/users/{1}'.format(
        os.getenv('ZAMMAD_URL_DOCKER'), user_data[3]), params=customParams, headers=customHeaders, json=customBody)

    print(reply.json())

    return JSONResponse({"message": "User modification successfully"})
