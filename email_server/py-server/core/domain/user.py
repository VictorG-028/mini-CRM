from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Optional, Any
import re
from uuid import UUID

@dataclass
class User:
    _id: Optional[UUID]
    created_at: Optional[datetime]
    client_full_name: str
    birth_date: date
    email: str
    telephone: Optional[str]
    cpf: str


    def __post_init__(self):
        # Validações básicas de domínio ao criar/carregar o objeto User
        if not self.client_full_name or len(self.client_full_name.strip()) < 3:
            raise ValueError("Full name must be at least 3 characters long.")
        if self.birth_date >= date.today():
            raise ValueError("Birth date cannot be in the future.")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format.")
        if not re.fullmatch(r"^\d{11}$", self.cpf): # Exemplo simples, CPF real precisa de mais
            raise ValueError("Invalid CPF format. Must be 11 digits.")
        if self.telephone and not re.fullmatch(r"^\+?\d{9,14}$", self.telephone):
            # https://gist.github.com/boliveirasilva/c927811ff4a7d43a0e0c
            raise ValueError("Invalid telephone format. Must be 9 to 14 digits, optionally starting with '+'.")

        # Auto define created_at both at database level and domain level
        if self._id is None and self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        data = asdict(self)

        if data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if data['birth_date']:
            data['birth_date'] = data['birth_date'].isoformat()
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]):

        # Converts back to date/datetime when loading from DB
        if isinstance(data.get("birth_date"), str):
            data["birth_date"] = date.fromisoformat(data["birth_date"])
        elif isinstance(data.get("birth_date"), datetime): # if DB returns datetime
            data["birth_date"] = data["birth_date"].date()
        else:
            print("investigar, pode ser um bug")

        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        user_id = str(data.get("_id"))

        return cls(
            _id=user_id,
            created_at=data.get("created_at"),
            client_full_name=data.get("client_full_name"),
            birth_date=data.get("birth_date"),
            email=data.get("email"),
            telephone=data.get("telephone"),
            cpf=data.get("cpf")
        )
