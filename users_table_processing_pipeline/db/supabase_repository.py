from typing import Optional
from uuid import UUID
from core.ports.driven_ports import ISenderBehaviorRepository, IUserRepository
from core.domain.email import Email
from core.domain.user import User
from core.domain.sender_behavior_enum import SenderBehaviorEnum
from core.domain.sender_behavior import SenderBehavior
from supabase import create_client, Client


class SupabaseRepository(ISenderBehaviorRepository, IUserRepository):
    def __init__(self, url: str, key: str):
       
        # https://supabase.com/docs/reference/python/initializing
        self._supabase: Client = create_client(url, key)
        self._users_table = self.get_users_table()
        self._sender_behavior_table = self.get_sender_behavior_table()


    def get_users_table(self) -> any:
        return self._supabase.table('users')
    
    def get_sender_behavior_table(self) -> any:
        return self._supabase.table('sender_behavior')

    ############################################################################
    #### --- Métodos de IUserRepository ---
    def save(self, user: User) -> None:
        user_dict = user.to_dict()
        
        if '_id' in user_dict: 
            del user_dict['_id']
        if 'created_at' in user_dict:
            del user_dict['created_at']
            
        response = self._users_table.insert(user_dict).execute()
        if response.data and len(response.data) > 0:
            user._id = str(response.data[0]['_id'])
        else:
            raise Exception(f"Failed to save user to Supabase: {response.error}")

    def update(self, user: User) -> None:
        if not user._id: 
            raise ValueError("User must have an ID to be updated.")
        
        update_data = user.to_dict()
        del update_data['_id']
        if 'created_at' in update_data: 
            del update_data['created_at']

        response = self._users_table.update(update_data).eq("_id", user._id).execute()
        if response.data is None or len(response.data) == 0:
            print(f"Warning: Supabase update for user {user._id} might not have affected any rows.")

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        response = self._users_table.select("*").eq("_id", user_id).limit(1).execute()
        if response.data and len(response.data) > 0:
            return User.from_dict(response.data[0])
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        response = self._users_table.select("*").eq("email", email).limit(1).execute()
        if response.data and len(response.data) > 0:
            return User.from_dict(response.data[0])
        return None

    def find_by_cpf(self, cpf: str) -> Optional[User]:
        response = self._users_table.select("*").eq("cpf", cpf).limit(1).execute()
        if not response.data or len(response.data) == 0:
            return None
        return User.from_dict(response.data[0])

    def find_all(self) -> list[User]:
        response = self._users_table.select("*").execute()
        if not response.data:
            return []
        return [User.from_dict(d) for d in response.data]

    def get_total_count(self) -> int:
        response = self._users_table.select("_id", count="exact").limit(0).execute()
        if response.count is None:
            return 0
        return response.count 

    def find_random_users(self, limit: int) -> list[User]:
        response = self._supabase.rpc(
            'get_random_users', 
            {'p_limit': limit}
        ).execute()
        # response = self._users_table.select("*").order("random()").limit(limit).execute()
        if not response.data:
            return []
        return [User.from_dict(d) for d in response.data]
    
    def find_random_users_by_birthday(self, limit: int) -> list[User]:
        response = self._supabase.rpc(
            'get_users_by_birthday', 
            {'p_limit': limit}
        ).execute()
        # response = self._users_table.select("*").eq("birth_date", "current_date").order("random()").limit(limit).execute()
        if not response.data:
            return []
        return [User.from_dict(d) for d in response.data]

    ############################################################################
    #### --- Métodos de ISenderBehaviorRepository ---

    def get_current_behavior(self) -> SenderBehaviorEnum:
        response = self._sender_behavior_table.select("strategy").limit(1).execute()
        if response.data and len(response.data) > 0:
            return SenderBehaviorEnum(response.data[0]['strategy'])
        return SenderBehaviorEnum.NOT_DEFINED
    
    
    def update_behavior(self, new_behavior: SenderBehaviorEnum) -> None:
        
        response = self._sender_behavior_table.select("_id").limit(1).execute()
        
        if response.data is None:
            raise Exception(f"Failed to fetch sender behavior from Supabase: {response.error}")
        
        first_line_exists = len(response.data) > 0
        if not first_line_exists:

            # Create first line
            insert_response = self._sender_behavior_table \
                .insert({"strategy": new_behavior.value}) \
                .execute()

            return

        # Else update existing line
        update_response = self._sender_behavior_table \
            .update({"strategy": new_behavior.value}) \
            .eq("_id", response.data[0]['_id']) \
            .execute()
