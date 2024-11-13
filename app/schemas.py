from pydantic import BaseModel

class UserCreate(BaseModel):
    # Define the fields for the UserCreate model
    username: str
    password: str

class UserResponse(BaseModel):
    # Define the fields for the UserResponse model
    id: int
    username: str

class Token(BaseModel):
    # Define the fields for the Token model
    access_token: str
    token_type: str
