from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
from uuid import UUID
from core.domain.email import Email
from core.domain.user import User
from core.domain.sender_behavior_enum import SenderBehaviorEnum

class IEmailSender(ABC):
    @abstractmethod
    def send(self, email: MIMEMultipart | MIMEText, to: str) -> bool:
        pass

class ISenderBehaviorRepository(ABC):
    @abstractmethod
    def get_current_behavior(self) -> SenderBehaviorEnum:
        pass
    @abstractmethod
    def update_behavior(self, new_behavior: SenderBehaviorEnum) -> None:
        pass

class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    @abstractmethod
    def update(self, user: User) -> None:
        pass
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[User]:
        pass
    @abstractmethod
    def get_total_count(self) -> int:
        pass
    @abstractmethod
    def find_random_users(self, limit: int) -> List[User]:
        pass
    @abstractmethod
    def find_random_users_by_birthday(self, limit: int) -> List[User]:
        pass

class ILogger(ABC):
    @abstractmethod
    def log_info(self, message: str) -> None:
        pass
    @abstractmethod
    def log_error(self, message: str, error: Optional[Exception] = None) -> None:
        pass
