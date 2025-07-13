from abc import ABC, abstractmethod
from uuid import UUID

from src.model.auth_token import AuthToken


class AuthTokenRepositoryInterface(ABC):
    @abstractmethod
    async def get_token_by_jti(self, jti: UUID) -> AuthToken | None:
        pass

    @abstractmethod
    async def create_token(self, jti: UUID, user_id: int) -> AuthToken:
        pass
