from tortoise import fields, models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    hashed_password = fields.CharField(128)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    async def create_user(cls, username: str, password: str):
        hashed_password = pwd_context.hash(password)
        return await cls.create(username=username, hashed_password=hashed_password)
