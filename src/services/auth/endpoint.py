from ..users.endpoint import createCustomer, getCustomer
from auth.auth_functions import generate_chatbot_token
from auth.middleware import VerifyTokenRoute
from db.usersDAO import usersDAO
from fastapi import APIRouter, Depends, Body
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from models.users.model import Customer
import json
from logs.setup import logger
from datetime import datetime

router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.post("/login")
async def login(authorization: str = Depends(token_auth_scheme), request: Request = None):

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
        + " - Doing loging..."
    )

    customer = json.loads(request.headers["customer"])
    customer = Customer(**customer)

    token = request.headers.get("api-authorization")
    username = customer.username

    user = usersDAO.get_user_data_by_username(username)

    if user is None:
        zammadCustomer = createCustomer(customer)
        if "error" in zammadCustomer:
            zammadCustomer = getCustomer(customer)

        usersDAO.create_user(username, token, zammadCustomer["id"])
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
            + " - New user created"
        )
        return JSONResponse({"message": "Login successfully"})
    else:
        usersDAO.update_user_data(username, token)
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
            + " - User updated"
        )
        return JSONResponse({"message": "Login successfully"})


@router.post("/logout")
async def logout(authorization: str = Depends(token_auth_scheme), request: Request = None):
    token = request.headers.get("api-authorization")
    usersDAO.remove_token_by_token(token)
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
        + " - User logged out"
    )
    return JSONResponse({"message": "Logout successfully"})


@router.post("/chatbot")
async def get_chatBot_token(authorization: str = Depends(token_auth_scheme), request: Request = None, locale: dict = Body(default="en-US")):

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
        + " - Generating chatbot token..."
    )

    token = request.headers.get("api-authorization")
    user = usersDAO.get_user_data_by_token(token)

    if user is not None:
        token = generate_chatbot_token(user[0], token, locale["locale"])
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
            + " - Chatbot token generated"
        )
        return token
    else:
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
            + " - 401 Unauthorized"
        )
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
