import asyncio
import datetime
from typing import Any, Literal
import numpy as np
import pandas as pd
# import matplotlib
from global_env_vars import (
    DATABASE_TYPE, 
    MONGO_DB_NAME, MONGO_URI, 
    SUPABASE_SECRET_KEY, SUPABASE_URL
)
from db.mongodb_repository import MongoDbRepository
from db.supabase_repository import SupabaseRepository

BIG_FILE_PATH = 'sensitive_data/big_PACIENTES.csv'
SMALL_FILE_PATH = 'sensitive_data/small_PACIENTES.csv'

################################################################################
#### Observando os datasets

def plot_columns_names(filepath: str, 
                       encoding: Literal['latin1', 'ISO-8859-1', 'Windows-1252'] = 'latin1'
                       ) -> None:
    try:
        # Read only the first row to get the headers
        df_head = pd.read_csv(filepath, nrows=0, encoding=encoding)
        print(f"Cabeçalhos do arquivo: {filepath}")
        for i, col in enumerate(df_head.columns):
            print(f"[{i+1:02d}] {col}")
            print("\n" + "="*30 + "\n")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em: {filepath}\n")
    except Exception as e:
        print(f"Erro ao ler o arquivo {filepath}: {e}\n")
    except Exception as e:
        print(f"Erro ao ler o arquivo {filepath}: {e}\n")

plot_columns_names(big_file)
plot_columns_names(small_file)

################################################################################
#### Escolhendo colunas e limpando as linhas

COLUMNS_TO_LOOK_FOR = {
    "client_full_name": ["nome", "nomecivil"],
    "birth_date": ["datanascimento"],
    "email": ["email"],
    "telephone": ["telefone_1", "telefone_2", "telefone_3", "telefone_4"], # Prioritizing multiple telephone columns
    "cpf": ["cpf"],
}

def clean_and_transform_dataframe(df: pd.DataFrame, file_type: Literal["big", "small"]) -> pd.DataFrame:
    processed_users = []
    
    column_mappings = COLUMNS_TO_LOOK_FOR
    df.columns = [col.lower().strip() for col in df.columns]

    for index, row in df.iterrows():
        user_data: dict[str, Any] = {}
        missing_essential_fields = False
        
        for user_field, csv_cols_options in column_mappings.items():
            found_value = None
            for col_name_option in csv_cols_options:
                if col_name_option in row and pd.notna(row[col_name_option]):
                    found_value = row[col_name_option]
                    break
            
            if user_field == "birth_date":
                if found_value:
                    try:
                        # Attempt DD/MM/YYYY first, then YYYY-MM-DD
                        if isinstance(found_value, str):
                            if '/' in found_value:
                                user_data[user_field] = datetime.strptime(found_value, "%d/%m/%Y").date().isoformat()
                            elif '-' in found_value:
                                user_data[user_field] = datetime.strptime(found_value, "%Y-%m-%d").date().isoformat()
                            else:
                                user_data[user_field] = None
                        elif isinstance(found_value, datetime):
                            user_data[user_field] = found_value.date().isoformat()
                        else:
                            user_data[user_field] = None
                    except ValueError:
                        user_data[user_field] = None
                        print(f"Warning: Row {index} - Could not parse birth_date '{found_value}'. Setting to None.")
                else:
                    user_data[user_field] = None

            elif user_field == "telephone":
                if found_value:
                    phone_str = str(found_value).strip()
                    if phone_str.startswith('+'):
                        phone_str = '+' + ''.join(filter(str.isdigit, phone_str))
                    else:
                        phone_str = ''.join(filter(str.isdigit, phone_str))
                    
                    user_data[user_field] = phone_str if phone_str else None
                else:
                    user_data[user_field] = None

            elif user_field == "cpf":
                if found_value:
                    cpf_str = str(found_value).replace(".", "").replace("-", "").strip()
                    if not cpf_str.isdigit() or len(cpf_str) != 11:
                        user_data[user_field] = None
                        print(f"Warning: Row {index} - Invalid CPF format '{found_value}'. Setting to None.")
                    else:
                        user_data[user_field] = cpf_str
                else:
                    user_data[user_field] = None
            
            elif found_value is not None:
                user_data[user_field] = str(found_value).strip()
            else:
                user_data[user_field] = None

        if not user_data.get("client_full_name") or \
           not user_data.get("birth_date") or \
           not user_data.get("email") or \
           not user_data.get("cpf"):
            missing_essential_fields = True
            print(f"Skipping row {index} due to missing essential data: {user_data}")

        if not missing_essential_fields:
            processed_users.append(user_data)

    return pd.DataFrame(processed_users)

################################################################################
#### Colocando no banco e dados


async def upload_to_supabase(users_df: pd.DataFrame, 
                             supabase_client: SupabaseRepository
                             ) -> None:
    
    assert supabase_client is not None, "Supabase client must be initialized."

    print(f"Attempting to upload {len(users_df)} users to Supabase...")
    table_name = 'users'
    users_data_list = users_df.to_dict(orient='records')

    try:
        response = await supabase_client.table(table_name).insert(users_data_list).execute()
        if response.error:
            print(f"Error uploading to Supabase: {response.error.message}")
        else:
            print(f"Successfully uploaded {len(response.data)} users to Supabase.")
    except Exception as e:
        print(f"Unexpected error during Supabase upload: {e}")

def upload_to_mongodb(users_df: pd.DataFrame, 
                      mongo_client: MongoDbRepository
                      ) -> None:
    
    assert mongo_client is not None, "MongoDB client must be initialized."

    print(f"Attempting to upload {len(users_df)} users to MongoDB...")
    db = mongo_client[MONGO_DB_NAME]
    collection = db['users']
    users_data_list = users_df.to_dict(orient='records')

    try:
        result = collection.insert_many(users_data_list)
        print(f"Successfully uploaded {len(result.inserted_ids)} users to MongoDB.")
    except Exception as e:
        print(f"Unexpected error during MongoDB upload: {e}")


if DATABASE_TYPE == "mongo":
    user_repository = MongoDbRepository(MONGO_URI, MONGO_DB_NAME)
    print("Using MongoDB for user and email repositories.")
elif DATABASE_TYPE == "supabase":
    user_repository = SupabaseRepository(SUPABASE_URL, SUPABASE_SECRET_KEY)
    print("Using Supabase for user and email repositories.")
else:
    raise ValueError("Invalid DATABASE_TYPE specified in environment variables.")

df_raw = pd.read_csv(BIG_FILE_PATH, encoding='latin1', sep=';')
df_processed = clean_and_transform_dataframe(df_raw.copy(), "big")

asyncio.run(upload_to_supabase(df_processed, supabase_client=user_repository))
# upload_to_mongodb(df_processed, mongo_client=user_repository)

