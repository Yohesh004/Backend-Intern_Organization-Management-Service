from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if hasattr(v, "binary"):
            return str(v)
        return str(v)

class OrgCreateRequest(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrgGetResponse(BaseModel):
    id: PyObjectId
    organization_name: str
    database_name: str
    admin_id: PyObjectId

class OrgUpdateRequest(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    new_organization_name: str = Field(..., min_length=3, max_length=50)

class OrgDeleteRequest(BaseModel):
    organization_name: str

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AdminCreateRecord(BaseModel):
    email: EmailStr
    hashed_password: str
    organization_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
