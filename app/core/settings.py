"""File with settings and configs for the project"""
from sqlalchemy.engine import URL


# connect string for the database:
# "postgresql+asyncpg://app_user:changeme@127.0.0.1:5432/app_db?ssl=disable"
DATABASE_IP = "127.0.0.1"
DATABASE_USER = "app_user"
DATABASE_PSWD = "changeme"
DATABASE_NAME = "app_db"

db_async_url = URL.create(
            "postgresql+asyncpg",
            username=DATABASE_USER,
            password=DATABASE_PSWD,
            host=DATABASE_IP,
            database=DATABASE_NAME,
            query={"ssl": "disable"},
)

db_url = URL.create(
            "postgresql",
            username=DATABASE_USER,
            password=DATABASE_PSWD,
            host=DATABASE_IP,
            database=DATABASE_NAME,
)

CDEK_URL = "https://api.cdek.ru/v2" # "https://api.edu.cdek.ru/v2"
CDEK_ID = "YOUR_CDEK_ACCOUNT" # "EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI"
CDEK_SECRET = "YOUR_CDEK_SECRET" # "PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG"

CRM_API = "YOUR_CRM_API_KEY"
CRM_URL = "https://example.retailcrm.ru/api/v5"

YADISK_TOKEN = "YOUR_YADISK_TOKEN"
