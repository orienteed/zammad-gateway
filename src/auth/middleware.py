from fastapi.routing import APIRoute
from fastapi import Request
from fastapi.responses import JSONResponse
from .auth_functions import validate_token, verify_token_db, update_date, update_token


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):

        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            if request.headers.get("Authorization") != None:
                if str(request.url).find("login") != -1:
                    validation_response = await validate_token(request)
                    if type(validation_response) == Request:
                        print('token valido')
                        return await original_route(request)
                    else:
                        print("token invalido")
                        return validation_response

                else:
                    verify_token_response = await verify_token_db(request)

                    if type(verify_token_response) is bool:
                        if verify_token_response:
                            print("fecha maxima sin validar en db y...")
                            validation_response = await validate_token(request)
                            if type(validation_response) == Request:
                                print('token valido')
                                update_date(
                                    request.headers["Authorization"].split(" ")[1])
                                return await original_route(request)
                            else:
                                print("token invalido")
                                return validation_response

                        else:
                            print("token sin expirar")
                            update_date(
                                request.headers["Authorization"].split(" ")[1])
                            return await original_route(request)

                    else:
                        if type(verify_token_response) == Request:
                            print('no está en db pero token valido')
                            token = request.headers["Authorization"].split(" ")[
                                1]
                            update_token(request.headers['username'], token)
                            return await original_route(request)
                        else:
                            print("token invalido")
                            print(verify_token_response)
                            return JSONResponse(content={"message": "Invalid token"}, status_code=401)

            else:
                return JSONResponse(content={"message": "Unauthorized, **no authorization header value**"}, status_code=401)

        return verify_token_middleware
