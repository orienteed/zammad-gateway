from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.router import api_router
from dotenv import load_dotenv
from metadata.tags_metadata import tags_metadata
from metadata.api_metadata import title, description, contact, version, license_info


def set_up():

	load_dotenv()

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(api_router, prefix="/api/v1")


app = FastAPI(title=title, description=description, contact=contact, version=version, license_info=license_info, openapi_tags=tags_metadata)
set_up()
