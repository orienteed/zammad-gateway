from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metadata.api_metadata import title, description, contact, version, license_info
from metadata.tags_metadata import tags_metadata
from services.router import api_router
from services.tickets.tickets_states.endpoint import update_states
import os
import requests


def initialTasks():
    # Create the organization
    customHeaders = {
        'Authorization': 'Token token={}'.format(os.getenv('ZAMMAD_API_KEY_DOCKER')),
        'Content-Type': 'application/json'
    }

    customBody = {
        'name': os.getenv('ORGANIZATION_NAME_DOCKER')
    }

    requests.post('{}/api/v1/organizations'.format(
        os.getenv('ZAMMAD_URL_DOCKER')), headers=customHeaders, json=customBody)

    
    # update active states
    update_states()


def set_up():
    load_dotenv()

    initialTasks()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/csr/api/v1")


app = FastAPI(title=title, description=description, contact=contact,
              version=version, license_info=license_info, openapi_tags=tags_metadata)
set_up()
