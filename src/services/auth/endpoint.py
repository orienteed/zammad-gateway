from urllib.request import Request
from fastapi import APIRouter, Body, Header
from auth.auth_functions import validate_token
from auth.middleware import VerifyTokenRoute
from ..users.endpoint import createCustomer
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from db.usersDAO import usersDAO

router = APIRouter(route_class=VerifyTokenRoute)


@router.get('/')
def login(Authorization: str = Header(None), username: dict = Body(default=""), request: Request = ""):   
    token = Authorization.split(" ")[1]
    username = username['username']
    
    # user = usersDAO.get_user_data(token)

    user = usersDAO.get_user_data_by_username_and_token(username, token)

    if user is None:
        usersDAO.create_user(username, token)
        return createCustomer(request)
        print("usuario creado")

    else:
        usersDAO.update_user_data(username, token)
        return JSONResponse({"login": "successfully"})
