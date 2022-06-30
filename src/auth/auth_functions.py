from urllib.request import Request
from fastapi.responses import JSONResponse
from requests import request
from db.usersDAO import usersDAO
from datetime import datetime, timedelta
from starlette.datastructures import MutableHeaders

def validate_token(token, request):
    print("validating token...")
    try:
        is_valid = True

        data = {"username": "juan@juan.com", "first_name": "juan", "last_name": "ito"}

        if is_valid:
            return modify_headers(request, token, data)

        else: 
            raise Exception

    except Exception:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)

def modify_headers(request, token, data):
    new_header = MutableHeaders(request._headers)
    new_header["username"]=data['username']
    new_header["first_name"]=data['first_name']
    new_header["last_name"]=data['last_name']
    request._headers = new_header
    
    usersDAO.update_user_data(data['username'], token)

    return request


def verify_token_db(token, request):
    user_data = usersDAO.get_user_data(token)
    if user_data is not None:
        print(user_data)
        # check_last_use_date(user_data[2], token)

        expired = is_expired(user_data[2])

        return expired


def is_expired(last_use_date):
    
    print("en check fecha")
    max_last_use_date = datetime.now() - timedelta(minutes=15)
    last_use_date = datetime.strptime(last_use_date, '%Y-%m-%d %H:%M:%S.%f')

    if max_last_use_date > last_use_date:
        return True
    else:
        return False


def update_date(token):
    usersDAO.update_user_data(token)
    
