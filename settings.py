# user_service - settings.py

from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Database configuration
DATABASE_URL = config("DATABASE_URL", cast=Secret)

# JWT settings
ALGORITHM = config.get("ALGORITHM")
SECRET_KEY = config.get("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_TIME= timedelta(days=int(config.get("ACCESS_TOKEN_EXPIRE_TIME")))

ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")
ADMIN_EXPIRY_TIME= timedelta(days=int(config.get("ADMIN_EXPIRY_TIME")))

# topics for produce and consume messages
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
NOTIFICATION_TOPIC = config.get("NOTIFICATION_TOPIC", cast=str)



