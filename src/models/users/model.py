from pydantic import BaseModel, EmailStr
from typing import Optional
import os


class Customer(BaseModel):
    username: EmailStr
    firstname: str
    lastname: str
    organization: str = os.getenv("ORGANIZATION_NAME_DOCKER")
    roles: str = "Customer"


class Customer_update(BaseModel):
    username: Optional[EmailStr]
    firstname: Optional[str]
    lastname: Optional[str]
