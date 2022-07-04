from urllib.request import Request
from dotenv import load_dotenv
from fastapi import APIRouter
import os
import requests
from auth.middleware import VerifyTokenRoute
from fastapi.requests import Request

load_dotenv()

# router = APIRouter()
router = APIRouter(route_class=VerifyTokenRoute)

# Get a customer
def getCustomer(expand: bool = False, X_On_Behalf_Of: str = None, request: Request = None):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'X-On-Behalf-Of': X_On_Behalf_Of,
        'expand': expand
    }

    reply = requests.get('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders)

    return reply.json()


# Create a customer
def createCustomer(request: Request):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customParams = {
        'expand': True
    }

    customBody = {
        "firstname": request.headers['first_name'],
        "lastname": request.headers['last_name'],
        "email": request.headers['username'],
        "login": request.headers['username'],
        "organization": 'B2BStore',
        "roles": ['Customer']
    }

    reply = requests.post('{}/api/v1/users'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), params=customParams, headers=customHeaders, json=customBody)

    return reply.json()
