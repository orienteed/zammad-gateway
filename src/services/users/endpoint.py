from auth.middleware import VerifyTokenRoute
from datetime import datetime
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from logs.setup import logger
from models.users.model import Customer, Customer_update
import os
import requests

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


def createCustomer(customer: Customer):

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": True}

    customBody = {
        "firstname": customer.firstname,
        "lastname": customer.lastname,
        "email": customer.username,
        "login": customer.username,
        "organization": customer.organization,
        "roles": customer.roles,
    }

    reply = requests.post(
        "{}/api/v1/users".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders, json=customBody
    )

    return reply.json()


def getCustomer(customer: Customer):
    customHeaders = {
        "Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")),
        "Content-Type": "application/json",
        "X-On-Behalf-Of": customer.username,
    }

    customParams = {
        "expand": True,
    }

    reply = requests.get("{}/api/v1/users".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders)

    return reply.json()[0]


@router.put("/")
def modify_customer(request: Request, authorization: str = Depends(token_auth_scheme), customer: Customer_update = None):

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
        + " - Updading customer..."
    )

    user_data = usersDAO.get_user_data_by_token(request.headers.get("csr-authorization"))

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": True}

    customBody = {"firstname": customer.firstname, "lastname": customer.lastname, "email": customer.username, "login": customer.username}

    reply = requests.put(
        "{0}/api/v1/users/{1}".format(os.getenv("ZAMMAD_URL_DOCKER"), user_data[3]),
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
        + " - Customer updated"
    )

    return JSONResponse({"message": "User modification successfully"})
