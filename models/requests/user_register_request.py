from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str