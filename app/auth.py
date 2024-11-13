from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from .models import User
from .config import SECRET_KEY, ALGORITHM

# Define the OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to authenticate a user
async def authenticate_user(username: str, password: str) -> User:
    # Retrieve the user by username
    user = await User.get_or_none(username=username)
    # Check if the user exists and the password is correct
    if not user or not user.verify_password(password):
        return None
    return user

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    # Create a copy of the data to encode
    to_encode = data.copy()
    # Set the expiration time for the token
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    # Add the expiration time to the data
    to_encode.update({"exp": expire})
    # Encode the data using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Return the encoded JWT
    return encoded_jwt
