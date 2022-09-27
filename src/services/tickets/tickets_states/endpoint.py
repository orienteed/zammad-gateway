from traceback import print_tb
from fastapi import APIRouter, Response, Depends
import os
import requests
import json
from fastapi.security import HTTPBearer
from auth.middleware import VerifyTokenRoute


router = APIRouter(route_class=VerifyTokenRoute)
token_auth_scheme = HTTPBearer()


@router.get("/")
def get_states(authorization: str = Depends(token_auth_scheme), expand: bool = False):

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customParams = {"expand": expand}

    reply = requests.get("{}/api/v1/ticket_states".format(os.getenv("ZAMMAD_URL_DOCKER")), params=customParams, headers=customHeaders)

    response = {}

    for group in reply.json():
        if group["active"] == True:
            response[group["id"]] = group["name"]

    return Response(content=json.dumps(response), media_type="application/json")


def update_states():

    activeStates = ["new", "open", "closed"]
    states = json.loads(get_states().body.decode())

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customBody = {"active": False}

    for state_id in states:
        if states[state_id] not in activeStates:
            reply = requests.put(
                "{}/api/v1/ticket_states/{}".format(os.getenv("ZAMMAD_URL_DOCKER"), state_id), headers=customHeaders, json=customBody
            )
