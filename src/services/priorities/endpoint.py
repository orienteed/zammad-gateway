from auth.middleware import VerifyTokenRoute
from fastapi import APIRouter, Response, Depends
from fastapi.security import HTTPBearer
import json
import os
import requests


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/")
def get_priorities(authorization: str = Depends(token_auth_scheme), expand: bool = False):

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": expand}

    reply = requests.get("{}/api/v1/ticket_priorities".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders)

    response = {}

    for group in reply.json():
        response[group["id"]] = group["name"].split(" ")[1]

    return Response(content=json.dumps(response), media_type="application/json")
