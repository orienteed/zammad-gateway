from fastapi import APIRouter, Response, Depends
import os
import requests
from fastapi.requests import Request
from datetime import datetime
import json
from fastapi.security import HTTPBearer
from auth.middleware import VerifyTokenRoute
from logs.setup import logger


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/")
def get_groups(request: Request, authorization: str = Depends(token_auth_scheme), expand: bool = False):

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
        + " - Fetching groups..."
    )

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": expand}

    reply = requests.get("{}/api/v1/groups".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders)

    response = {}

    for group in reply.json():
        response[group["id"]] = group["name"]

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
        + " - Groups fetched"
    )

    return Response(content=json.dumps(response), media_type="application/json")
