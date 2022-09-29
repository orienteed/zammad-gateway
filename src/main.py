from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metadata.api_metadata import title, description, contact, version, license_info
from metadata.tags_metadata import tags_metadata
from services.router import api_router
from services.tickets.tickets_states.endpoint import update_states
from services.organizations.endpoint import update_organization
from logs.setup import logger
import os
import requests


def initialTasks():

    # Create the organization
    update_organization()

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


app = FastAPI(title=title, description=description, contact=contact, version=version, license_info=license_info, openapi_tags=tags_metadata)
set_up()
