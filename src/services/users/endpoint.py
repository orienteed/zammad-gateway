from fastapi import APIRouter
import os
import requests
from auth.middleware import VerifyTokenRoute
from models.users.model import Customer


router = APIRouter(route_class=VerifyTokenRoute)

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
