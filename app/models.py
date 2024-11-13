from tortoise import fields, models
from passlib.context import CryptContext
    
# Create an instance of CryptContext with the bcrypt scheme and deprecated set to auto
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(models.Model):
    # Define the fields for the User model
    id: int = fields.IntField(pk=True)  # Primary key field
    username: str = fields.CharField(max_length=50, unique=True)  # Username field with a maximum length of 50 characters and uniqueness constraint
    hashed_password: str = fields.CharField(max_length=128)  # Hashed password field with a maximum length of 128 characters

    # Method to verify the provided password against the stored hashed password
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    # Class method to create a new user with the provided username and password
    @classmethod
    async def create_user(cls, username: str, password: str) -> 'User':
        # Hash the password using bcrypt
        hashed_password = pwd_context.hash(password)
        # Create and return a new User instance with the hashed password
        return await cls.create(username=username, hashed_password=hashed_password)
    