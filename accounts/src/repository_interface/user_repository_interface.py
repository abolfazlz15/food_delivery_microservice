from abc import ABC, abstractmethod
from src.schema.user import UserUpdateProfileInDBSchema
from src.model.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_user_detail_by_id(self, id: int) -> User | None:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, **user_data: UserUpdateProfileInDBSchema) -> User | None:
        pass