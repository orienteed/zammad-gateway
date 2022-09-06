from fastapi.routing import APIRoute
from fastapi import Request
from fastapi.responses import JSONResponse

from models.users.model import Customer
from .auth_functions import validate_token, verify_token_db, update_date, update_token, modify_headers


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):

        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            if request.headers.get("csr-authorization") != None:
                token = request.headers.get("csr-authorization")
                if str(request.url).find("login") != -1:
                    return await process_validate_token(request, token, original_route)

                else:
                    verify_token_response = await verify_token_db(token)

                    if type(verify_token_response) is bool:
                        return await process_token_exist_db(request, token, verify_token_response, original_route)

                    else:
                        return await process_token_not_exist_db(request, token, verify_token_response, original_route)

            else:
                return JSONResponse(content={"message": "Unauthorized, **no authorization header value**"}, status_code=401)

        return verify_token_middleware


async def process_validate_token(request, token, original_route, update_token_date=False):
    validation_response = await validate_token(token)

    if type(validation_response) == Customer:
        print('Valid token')
        if update_token_date:
            update_date(token)
            print("Token date updated")
            return await original_route(request)
        else:
            modify_request = modify_headers(request, validation_response)
            return await original_route(modify_request)

    else:
        print("Invalid token")
        return validation_response


async def process_token_exist_db(request, token, token_is_expired, original_route):
    if token_is_expired:
        print("Maximum time without token validation")
        return await process_validate_token(request, token, original_route, update_token_date=True)

    else:
        print("Unexpired token")
        update_date(token)
        return await original_route(request)


async def process_token_not_exist_db(request, token, verify_token_response, original_route):
    if type(verify_token_response) == Customer:
        print('the token is not in the db but it is valid')
        update_token(verify_token_response.username, token)
        return await original_route(request)

    else:
        print("Invalid token")
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)
