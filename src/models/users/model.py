from pydantic import BaseModel, EmailStr
from typing import Optional

class Customer(BaseModel):
    username: EmailStr
    firstname: str
    lastname: str
    organization: str ="B2BStore"
    roles: str = "Customer"