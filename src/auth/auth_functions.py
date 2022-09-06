from .graphql.validate_token import magento_validate_token
from calendar import c
from datetime import datetime, timedelta
from db.usersDAO import usersDAO
from dotenv import load_dotenv
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from models.users.model import Customer
from starlette.datastructures import MutableHeaders
import json
import os
import jwt

load_dotenv()


def modify_headers(request: Request, customer: Customer):
    print("Modifying headers...")

    new_header = MutableHeaders(request._headers)
    new_header['customer'] = json.dumps(customer.dict())
    request._headers = new_header

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

    customer_data['customer']['username'] = customer_data['customer'].pop(
        'email')
    customer = Customer(**customer_data['customer'])

    return customer


def generate_chatbot_token(email):

    payload = {
        'sub': 'a3e036a3-33d6-4ab6-b4c9-6b1b3db8bb01',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=600),
        'attributes': {"email": email}
    }

    header = {
        'typ': "JWT",
        'alg': 'HS256'
    }

    encoded_token = jwt.encode((payload), os.getenv('CHATBOT_SECURITY_KEY_DOCKER'), algorithm="HS256", headers=header)

    return encoded_token