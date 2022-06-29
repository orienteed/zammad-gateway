from dotenv import load_dotenv
from fastapi import APIRouter, Header, Response
import os
import requests
import json

load_dotenv()

router = APIRouter()

# Get states
@router.get('/')
def getStates(Authorization: str | None = Header(default="")):

    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    reply = requests.get('{}/api/v1/ticket_states'.format(os.getenv('ZAMMAD_URL_DOCKER')), headers=customHeaders)

    response = {}

    for group in reply.json():
        response[group['id']] = group['name']

    return Response(content=json.dumps(response))