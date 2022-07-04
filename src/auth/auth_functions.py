import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from db.usersDAO import usersDAO
from datetime import datetime, timedelta
from starlette.datastructures import MutableHeaders
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from .graphql.validate_token import magento_validate_token

load_dotenv()


def modify_headers(request, token, data):
    print("Modifying headers...")
    new_header = MutableHeaders(request._headers)
    new_header["username"] = data['email']
    new_header["first_name"] = data['firstname']
    new_header["last_name"] = data['lastname']
    request._headers = new_header

    return request


async def verify_token_db(request):
    token = request.headers["Authorization"].split(" ")[1]
    user_data = usersDAO.get_user_data_by_token(token)
    if user_data is not None:
        expired = is_expired(user_data[2])
        return expired

    else:
        return await validate_token(request)


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


async def validate_token(request):
    print("validating token...")
    token = request.headers["Authorization"]
    transport = AIOHTTPTransport(url=os.getenv(
        'MAGENTO_URL_DOCKER'), headers={'Authorization': token})
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = magento_validate_token()

    try:
        result = await client.execute_async(query)
        print(result)

    except Exception as e:
        print("invalid token...")
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)

    return modify_headers(request, token, result['customer'])

    # try:

    #     if result is not None:
    #         if result.get('message') is not None:
    #             raise Exception

    #         return modify_headers(request, token, result['customer'])    
    #     else:
    #         raise Exception

    # except Exception:
    #     return JSONResponse(content={"message": "Invalid Token"}, status_code=401)

    
    
    
