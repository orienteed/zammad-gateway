from ensurepip import version


title = "Zammad Gateway"
description = """ Intermediate API endpoint that encapsulates/handles the authentication and request to the Zammad API (like a wrapper) and exposes a single, dedicated endpoint for POSTing the payloads.
## Authentication

Before all, you must **Authenticate it**.

## Tickets

You will be able to:

* **Create tickets**
* **List tickets**
* **View ticket comments**
* **Download ticket attachments**
* **Update the state of a ticket**

## State

You will be able to:

* **List ticket states**

## Groups

You will be able to:

* **List groups**

## Priorities

You will be able to:

* **List priorities**

"""

version = "2.0.0"
contact = {"name": "Orienteed", "url": "https://www.orienteed.com"}
license_info = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
