from fastapi import APIRouter, Header, Body
import os
import requests

router = APIRouter()

# Get a customer


@router.get('/')
def getCustomer(expand: bool = False, X_On_Behalf_Of: str = None, Authorization: str | None = Header(default="")):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_ADMIN_API_KEY')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'X-On-Behalf-Of': X_On_Behalf_Of,
		'expand': expand
    }

    reply = requests.get('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL')), params=customParams, headers=customHeaders)

    return reply.json()


# Create a customer
@router.post('/')
def createCustomer(expand: bool = False, firstname: str = Body(default=""), lastname: str = Body(default=""),
                   email: str = Body(default=""), login: str = Body(default=""), organization: str = Body(default="B2BStore"),
                   roles: list = Body(default=["Customer"]), Authorization: str | None = Header(default="")):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_ADMIN_API_KEY')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': expand
    }

    customBody = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "login": login,
        "organization": organization,
        "roles": roles
    }

    reply = requests.get('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL')), params=customParams, headers=customHeaders, json=customBody)

    return reply.json()
