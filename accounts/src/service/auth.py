from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import UserRepository
from src.schema.user import UserInDBSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> UserInDBSchema | None:
    user_dict = await UserRepository(session).get_user_by_email(email=email)
    if not user_dict:
        return None
    user = UserInDBSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
    )
    if not verify_password(password, user.password):
        return None
    return user



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches its hashed counterpart.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    """
    return pwd_context.hash(password)
