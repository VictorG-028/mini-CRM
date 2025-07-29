import os
from dotenv import load_dotenv
from datetime import datetime
import locale


################################################################################
#### Secret global environment variables

load_dotenv()

GOOGLE_EMAIL_API_KEY = os.environ.get('GOOGLE_EMAIL_API_KEY')
# HOSTINGER_EMAIL_PASSWORD = os.environ.get('HOSTINGER_EMAIL_PASSWORD')
GOOGLE_SENDER_EMAIL = os.environ.get('GOOGLE_SENDER_EMAIL')
GOOGLE_SENDER_PASSWORD = os.environ.get('GOOGLE_SENDER_PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
GOOGLE_EMAIL_CLIENT_ID = os.environ.get('GOOGLE_EMAIL_CLIENT_ID')


# Database credentials
# GOOGLE_DRIVE_API_KEY = os.environ.get('GOOGLE_DRIVE_API_KEY')

# SUPABASE_DB_PASSWORD = os.environ.get('SUPABASE_DB_PASSWORD')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_SECRET_KEY = os.environ.get('SUPABASE_SECRET_KEY')
# SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
# SUPABASE_PROJECT_KEY = os.environ.get('SUPABASE_PROJECT_KEY')
SUPABASE_USER = os.getenv("user")
SUPABASE_PASSWORD = os.getenv("password")
SUPABASE_HOST = os.getenv("host")
SUPABASE_PORT = os.getenv("port")
SUPABASE_DBNAME = os.getenv("dbname")

MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB_USER = os.environ.get('MONGO_DB_USER')
MONGO_DB_PASSWORD = os.environ.get('MONGO_DB_PASSWORD')
MONGO_DB_CODE = os.environ.get('MONGO_DB_CODE')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')

################################################################################
#### Administrator global environment variables

def _convert_to_list(value: str) -> list[str]:
    """
    "some@string" -> ['some@string'] \n
    "some@string,other@string" -> ['some@string', 'other@string'] \n
    """
    return value.split(",")

def _convert_to_bool(value: str) -> bool:
    return value == "True"

def _convert_to_int(value: str)-> int:
    return int(value)

SERVER_PORT = _convert_to_int(os.environ.get('SERVER_PORT', 8000))
DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'supabase') # mongodb or supabase
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'espaco.pamela@gmail.com.br')
IS_PROD = _convert_to_bool(os.environ.get('IS_PROD', True))

################################################################################
#### Generated global environment variables

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') # Makes datetime lib spit string in a non default format

START_TIME = datetime.now()
CURRENT_DATE = START_TIME.strftime('%d/%m/%Y') # day/month/year
WEEKDAY: str = START_TIME.strftime('%A') # segunda, terça, quarta, quinta, sexta, sábado, domingo 

################################################################################
