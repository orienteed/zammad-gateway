from email.quoprimime import body_decode
from wsgiref import headers
from wsgiref.util import request_uri
from fastapi.routing import APIRoute
from fastapi import Request
from .auth_functions import validate_token, verify_token_db, update_date, modify_headers
from starlette.datastructures import MutableHeaders


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        
        original_route = super().get_route_handler()
        async def verify_token_middleware(request:Request):
            token = request.headers["Authorization"].split(" ")[1]

            if str(request.url).find("login") != -1:
                try:                    
                    validation_response = await validate_token(request)
                    if type(validation_response) == Request:
                        print('token valido')
                        return await original_route(request)
                    else:
                        print("token invalido")
                        return validation_response

                except Exception as ke:
                    print(original_route)

            else:
                verification_response = verify_token_db(request)

                if verification_response:
                    print("El token ha expirado")
                    validation_response = await validate_token(request)
                    if type(validation_response) == Request:
                        print('token valido')
                        update_date(request.headers["Authorization"].split(" ")[1])
                        return await original_route(request)
                    else:
                        print("token invalido")
                        return validation_response

                else:
                    print("token sin expirar")
                    update_date(request.headers["Authorization"].split(" ")[1])
                    return await original_route(request)

        return verify_token_middleware
