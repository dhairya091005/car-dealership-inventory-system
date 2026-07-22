from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


# Alias used by routes
UserCreate = UserRegister


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
