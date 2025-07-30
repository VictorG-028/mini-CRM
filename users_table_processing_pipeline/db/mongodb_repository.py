# py-server/adapters/driven/db/mongodb_repository.py
from core.ports.driven_ports import ISenderBehaviorRepository, IUserRepository # ATUALIZADO
from core.domain.email import Email
from core.domain.user import User # NOVO
from pymongo import MongoClient
from typing import List, Optional
from bson.objectid import ObjectId # Para converter IDs de/para MongoDB

class MongoDbRepository(ISenderBehaviorRepository, IUserRepository):
    def __init__(self, connection_string: str, db_name: str):
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]
        self._emails_collection = self._db['emails']
        self._users_collection = self._db['users'] # NOVA COLEÇÃO para usuários

    # Métodos de IEmailRepository (como antes)
    def save(self, email: Email) -> None:
        email_dict = email.to_dict()
        self._emails_collection.insert_one(email_dict)
    # ... find_by_id, find_all para Email

    # Métodos de IUserRepository (NOVOS)
    def save(self, user: User) -> None: # Sobrescreve save? Cuidado! Mude o nome ou separe.
                                         # Melhor: renomeie para save_email e save_user
                                         # Ou: crie classes separadas
        user_dict = user.to_dict()
        result = self._users_collection.insert_one(user_dict)
        user._id = str(result.inserted_id) # Atribui o ID gerado pelo MongoDB

    def update(self, user: User) -> None:
        if not user._id: 
            raise ValueError("User must have an ID to be updated.")

        user_dict = user.to_dict()
        if '_id' in user_dict: 
            del user_dict['_id']

        self._users_collection.update_one(
            {"_id": ObjectId(user._id)},
            {"$set": user_dict}
        )

    def find_by_id(self, user_id: str) -> Optional[User]:
        data = self._users_collection.find_one({"_id": ObjectId(user_id)})
        return User.from_dict(data) if data else None

    def find_by_email(self, email: str) -> Optional[User]:
        data = self._users_collection.find_one({"email": email})
        return User.from_dict(data) if data else None

    def find_all(self) -> List[User]:
        return [User.from_dict(d) for d in self._users_collection.find()]
