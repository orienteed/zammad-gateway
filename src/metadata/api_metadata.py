from ensurepip import version


title = "Zammad Gateway"
description = """
## What is Zammad Gateway?
Zammad Gateway is an excellent tool for those who want to integrate Zammad with external systems but don't have the knowledge or time to develop a custom integration.

It is an intermediate API that encapsulates/handles the authentication and requests to the Zammad Helpdesk API (like a wrapper) and exposes some endpoints to interact with them. The Gateway is a straightforward and effective way to integrate Zammad with third-party systems.

This software can be installed on a server and configured to listen for incoming requests from external systems. It then forwards those requests to Zammad using the Zammad Helpdesk API.

## How does it work?

You should use the header 'api-authorization' with the Magento Customer token value to authenticate the requests.


"""

version = "2.0.0"
contact = {"name": "Orienteed", "url": "https://www.orienteed.com"}
license_info = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
