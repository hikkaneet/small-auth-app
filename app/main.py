from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import authenticate_user, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, TORTOISE_ORM

# Create the FastAPI application instance
app = FastAPI()

# Endpoint to authenticate users and return an access token
@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user using the provided username and password
    user = await authenticate_user(form_data.username, form_data.password)
    # If authentication fails, raise an HTTP exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Calculate the expiration time for the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create the access token using the user's username and expiration time
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to create a new user
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Check if a user with the same username already exists
    existing_user = await User.get_or_none(username=user.username)
    # If the user exists, raise an HTTP exception
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Create a new user with the provided username and password
    new_user = await User.create_user(username=user.username, password=user.password)
    # Return the ID and username of the newly created user
    return {"id": new_user.id, "username": new_user.username}

# Register Tortoise ORM with the FastAPI app to connect to the database
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Automatically generate schemas based on the models
    add_exception_handlers=True,  # Add exception handlers for Tortoise ORM errors
)

# CORS settings
origins = [                     # Frontend address list
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allowed sources
    allow_credentials=True,
    allow_methods=["*"],        # Allow all methods (GET, POST и т.д.)
    allow_headers=["*"],        # Allow all headers
)
