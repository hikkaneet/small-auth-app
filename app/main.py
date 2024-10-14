from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import authenticate_user, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, TORTOISE_ORM

app = FastAPI()

@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await User.get_or_none(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = await User.create_user(username=user.username, password=user.password)
    return {"id": new_user.id, "username": new_user.username}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

# Настройте CORS
origins = [
    "http://localhost:5173",  # добавьте адрес фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # разрешить все заголовки
)