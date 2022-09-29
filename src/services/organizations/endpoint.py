from datetime import datetime
import requests
import os
from datetime import datetime

from logs.setup import logger


def update_organization():

    customHeaders = {"Authorization": "Token token={}".format(os.getenv("ZAMMAD_API_KEY_DOCKER")), "Content-Type": "application/json"}

    customBody = {"name": os.getenv("ORGANIZATION_NAME_DOCKER")}

    reply = requests.post("{}/api/v1/organizations".format(os.getenv("ZAMMAD_URL_DOCKER")), headers=customHeaders, json=customBody)

    if "error" in reply.json():
        logger.info("WARNING - [" + str(datetime.now()) + "]: Create Organization - " + str(reply.json()))

    else:
        logger.info("INFO    - [" + str(datetime.now()) + "]: Organization created: {}".format(reply.json()))
