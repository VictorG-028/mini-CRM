# py-server/core/ports/driving_ports.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID
from core.domain.email import Email
from core.domain.user import User
from core.domain.sender_behavior_enum import SenderBehaviorEnum
from core.domain.template_catalog_enum import TemplateCatalogEnum

class IEmailService(ABC):
    @abstractmethod
    def send_emails(self, count: int, template_name: TemplateCatalogEnum, fill_values: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def change_sender_behavior(self, new_behavior: SenderBehaviorEnum) -> None:
        pass

    @abstractmethod
    def get_sender_behavior(self) -> SenderBehaviorEnum:
        pass


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: UUID, user_data: Dict[str, Any]) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_total_users(self) -> Optional[User]:
        pass

    # TODO
    # @abstractmethod
    # def get_user_by_email(self, email: str) -> Optional[User]:
    #     pass

    # @abstractmethod
    # def get_all_users(self) -> List[User]:
    #     pass
