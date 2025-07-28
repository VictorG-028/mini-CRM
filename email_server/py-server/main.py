from fastapi import FastAPI
from adapters.driving.http_adapter import HTTPAdapter
from adapters.driven.smtp_adapter import SmtpAdapter
from adapters.driven.logger_adapter import ConsoleLogger
from adapters.driven.db.mongodb_repository import MongoDbRepository
from adapters.driven.db.supabase_repository import SupabaseRepository
from core.services.email_service import EmailService
from core.services.user_service import UserService
from config.global_env_vars import (
    DATABASE_TYPE,
    IS_PROD, 
    MONGO_URI, MONGO_DB_NAME, 
    SUPABASE_URL, SUPABASE_SECRET_KEY
    # USER, PASSWORD, HOST, PORT, DBNAME
)
# from starlette.middleware.errors import ServerErrorMiddleware
# from starlette.middleware.exceptions import DebugMiddleware

app = FastAPI()

if not IS_PROD:
    # app.add_middleware(ServerErrorMiddleware)
    # app.add_middleware(DebugMiddleware)
    pass

# Output adapters
logger = ConsoleLogger()
email_sender = SmtpAdapter(logger)
user_repository = None
sender_behavior_repository = None

if DATABASE_TYPE == "mongo":
    db_connector = MongoDbRepository(MONGO_URI, MONGO_DB_NAME)
    user_repository = db_connector
    sender_behavior_repository = db_connector
    logger.log_info("Using MongoDB for user and email repositories.")
elif DATABASE_TYPE == "supabase":
    db_connector = SupabaseRepository(SUPABASE_URL, SUPABASE_SECRET_KEY)
    user_repository = db_connector
    sender_behavior_repository = db_connector
    logger.log_info("Using Supabase for user and email repositories.")
else:
    raise ValueError("Invalid DATABASE_TYPE specified in environment variables.")

# Services
user_service = UserService(
    user_repository=user_repository, 
    logger=logger
)
email_service = EmailService(
    email_sender=email_sender,
    sender_behavior_repository=sender_behavior_repository,
    user_repository=user_repository,
    logger=logger
)

# Input Adapters
http_adapter = HTTPAdapter(
    email_service=email_service, 
    user_service=user_service
)

# Bind endpoints
app.include_router(http_adapter.router)

# Execute the application
# uvicorn: uvicorn main:app --reload --port 7999
