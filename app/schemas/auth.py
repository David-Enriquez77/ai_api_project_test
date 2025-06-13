from pydantic import BaseModel
#Schemas for authentication-related data
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    username: str
    password: str
