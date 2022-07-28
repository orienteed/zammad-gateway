from calendar import c
import os
from wsgiref import headers
from fastapi.requests import Request
from urllib.request import Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import requests
from db.usersDAO import usersDAO
from datetime import datetime, timedelta
from starlette.datastructures import MutableHeaders
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from models.users.model import Customer
from .graphql.validate_token import magento_validate_token
import json

load_dotenv()


def modify_headers(request: Request, customer: Customer):
    print("Modifying headers...")
    
    new_header = MutableHeaders(request._headers)
    new_header['customer'] = json.dumps(customer.dict())
    request._headers = new_header
    # request._body = json.dumps({"authorization": token, "username": data['email'], "firstname": data['firstname'], "lastname": data['lastname']})
    
    print("headers modified")

    return request


async def verify_token_db(token):
    user_data = usersDAO.get_user_data_by_token(token)
    if user_data is not None:
        expired = is_expired(user_data[2])
        return expired

    else:
        return await validate_token(token)


def is_expired(last_use_date):
    max_last_use_date = datetime.now() - timedelta(minutes=15)
    last_use_date = datetime.strptime(last_use_date, '%Y-%m-%d %H:%M:%S.%f')

    if max_last_use_date > last_use_date:
        return True
    else:
        return False


def update_date(token):
    print("updating last use date")
    usersDAO.update_token_date(token)


def update_token(username, token):
    print("updating token...")
    usersDAO.update_user_data(username, token)


async def validate_token(token):
    print("validating token...")
    transport = AIOHTTPTransport(url=os.getenv(
        'MAGENTO_URL_DOCKER'), headers={'Authorization': 'Bearer ' + token})
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = magento_validate_token()

    try:
        customer_data = await client.execute_async(query)

    except Exception as ex:
        print("invalid token...")
        print(ex)
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)

    customer_data['customer']['username'] = customer_data['customer'].pop('email')
    customer = Customer(**customer_data['customer'])

    return customer
