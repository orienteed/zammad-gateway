from urllib.request import Request
from fastapi import APIRouter, Body, Header
from auth.auth_functions import validate_token
from auth.middleware import VerifyTokenRoute
from ..users.endpoint import createCustomer
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from db.usersDAO import usersDAO

router = APIRouter(route_class=VerifyTokenRoute)


@router.post('/')
def login(Authorization: str = Header(None), request: Request = ""):
    token = Authorization.split(" ")[1]
    username = request.headers['username']

    user = usersDAO.get_user_data_by_username(username)

    if user is None:
        usersDAO.create_user(username, token)

        createCustomer(request)

        return JSONResponse({"message": "Login successfully"})

    else:
        usersDAO.update_user_data(username, token)
        return JSONResponse({"message": "Login successfully"})
