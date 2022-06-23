from imp import reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.router import api_router
import uvicorn


def set_up():

	app = FastAPI()

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(api_router)

	uvicorn.run(app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
	set_up()
