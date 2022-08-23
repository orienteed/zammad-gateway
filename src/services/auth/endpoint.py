from fastapi import APIRouter, Depends
from auth.middleware import VerifyTokenRoute
from ..users.endpoint import createCustomer, getCustomer
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from db.usersDAO import usersDAO
from models.users.model import Customer
import json

router = APIRouter(route_class=VerifyTokenRoute)

token_auth_scheme = HTTPBearer()


@router.post('/')
async def login(authorization: str = Depends(token_auth_scheme), request: Request = None):

    customer = json.loads(request.headers["customer"])
    customer = Customer(**customer)

    token = authorization.credentials
    username = customer.username

    user = usersDAO.get_user_data_by_username(username)

    if user is None:
        zammadCustomer = createCustomer(customer)
        if 'error' in zammadCustomer:
            zammadCustomer = getCustomer(customer)

        usersDAO.create_user(username, token, zammadCustomer['id'])
        return JSONResponse({"message": "Login successfully"})
    else:
        usersDAO.update_user_data(username, token)
        return JSONResponse({"message": "Login successfully"})
