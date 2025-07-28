# py-server/core/services/user_service.py
from uuid import UUID
from core.ports.driving_ports import IUserService
from core.ports.driven_ports import IUserRepository, ILogger
from core.domain.user import User
from typing import Any, Optional

class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, logger: ILogger):
        self._user_repository = user_repository
        self._logger = logger

    def create_user(self, user_data: dict[str, Any]) -> User:
        
        # Validação
        if self._user_repository.find_by_email(user_data["email"]):
            raise ValueError("User with this email already exists.")
        if self._user_repository.find_by_cpf(user_data["cpf"]):
            raise ValueError("User with this CPF already exists.")

        # Criação (CPU)
        try:
            user = User(_id=None, created_at=None, **user_data)
        except ValueError as e:
            raise ValueError(f"Invalid user data: {e}")

        # Banco de dados (IO)
        self._user_repository.save(user)
        
        self._logger.log_info(f"User created: user_data={user_data}")
        return user

    def update_user(self, 
                    user_id: UUID, 
                    user_data: dict[str, Any]
                    ) -> Optional[User]:
        
        # Validação
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        
        if "email" in user_data and user_data["email"] != user.email:
            if self._user_repository.find_by_email(user_data["email"]):
                raise ValueError("New email already exists for another user.")
        if "cpf" in user_data and user_data["cpf"] != user.cpf:
            if self._user_repository.find_by_cpf(user_data["cpf"]):
                raise ValueError("New CPF already exists for another user.")

        # Atualizar campos in memory
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        # validação pós-atualização
        try:
            user.__post_init__()
        except ValueError as e:
            raise ValueError(f"Invalid updated user data: {e}")

        self._user_repository.update(user)
        self._logger.log_info(f"User updated: {user.email}")
        return user

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self._user_repository.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self._user_repository.find_by_email(email)

    def get_total_users(self) -> int:
        return self._user_repository.get_total_count()
