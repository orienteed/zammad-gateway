from .auth_functions import validate_token, verify_token_db, update_date, update_token, modify_headers
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from logs.setup import logger
from models.users.model import Customer


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):

        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            if request.headers.get("api-authorization") != None:
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
                )
                token = request.headers.get("api-authorization")
                if str(request.url).find("login") != -1:
                    return await process_validate_token(request, token, original_route)

                else:
                    verify_token_response = await verify_token_db(token, request)

                    if type(verify_token_response) is bool:
                        return await process_token_exist_db(request, token, verify_token_response, original_route)

                    else:
                        return await process_token_not_exist_db(request, token, verify_token_response, original_route)

            else:
                logger.info(
                    "ERROR   - ["
                    + str(datetime.now())
                    + "]: "
                    + str(request.client.host)
                    + ":"
                    + str(request.client.port)
                    + " - "
                    + str(request.method)
                    + " - "
                    + str(request.url.path)
                    + " - 401 Unauthorized - Token not found"
                )
                return JSONResponse(content={"message": "Unauthorized, **no authorization header value**"}, status_code=401)

        return verify_token_middleware


async def make_request(request, original_route):
    try:
        response = await original_route(request)
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
            + " - "
            + str(response.status_code)
        )
        return response

    except Exception as e:
        logger.info(
            "ERROR   - ["
            + str(datetime.now())
            + "]: "
            + str(request.client.host)
            + ":"
            + str(request.client.port)
            + " - "
            + str(request.method)
            + " - "
            + str(request.url.path)
            + " - "
            + str(e)
        )
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)


async def process_validate_token(request, token, original_route, update_token_date=False):
    validation_response = await validate_token(token, request)

    if type(validation_response) == Customer:
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
            + " - 200 OK - Token validated"
        )
        if update_token_date:
            update_date(token)
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
                + " - Token last date use updated"
            )

            return await make_request(request, original_route)

        else:
            modify_request = modify_headers(request, validation_response)
            return await make_request(modify_request, original_route)

    else:
        logger.info(
            "ERROR   - ["
            + str(datetime.now())
            + "]: "
            + str(request.client.host)
            + ":"
            + str(request.client.port)
            + " - "
            + str(request.method)
            + " - "
            + str(request.url.path)
            + " - 401 Unauthorized - Invalid token"
        )
        return validation_response


async def process_token_exist_db(request, token, token_is_expired, original_route):
    if token_is_expired:
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
            + " - Maximum time without token validation"
        )
        return await process_validate_token(request, token, original_route, update_token_date=True)

    else:
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
            + " - Unexpired token"
        )
        update_date(token)
        return await make_request(request, original_route)


async def process_token_not_exist_db(request, token, verify_token_response, original_route):
    if type(verify_token_response) == Customer:
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
            + " - Updating token in database..."
        )
        update_token(verify_token_response.username, token)
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
            + " - Token updated in database"
        )

        return await make_request(request, original_route)

    else:
        logger.info(
            "ERROR   - ["
            + str(datetime.now())
            + "]: "
            + str(request.client.host)
            + ":"
            + str(request.client.port)
            + " - "
            + str(request.method)
            + " - "
            + str(request.url.path)
            + " - 401 Unauthorized - Invalid token"
        )
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)
