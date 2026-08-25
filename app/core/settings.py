"""File with settings and configs for the project"""
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


DATABASE_IP = os.getenv("DATABASE_IP", "127.0.0.1")
DATABASE_USER = os.getenv("DATABASE_USER", "app_user")
DATABASE_PSWD = os.getenv("DATABASE_PSWD", "changeme")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

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

# CDEK sandbox defaults are the public demo credentials from CDEK docs.
CDEK_URL = os.getenv("CDEK_URL", "https://api.edu.cdek.ru/v2")
CDEK_ID = os.getenv("CDEK_ID", "EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI")
CDEK_SECRET = os.getenv("CDEK_SECRET", "PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG")

CRM_API = os.getenv("CRM_API", "YOUR_CRM_API_KEY")
CRM_URL = os.getenv("CRM_URL", "https://example.retailcrm.ru/api/v5")

YADISK_TOKEN = os.getenv("YADISK_TOKEN", "YOUR_YADISK_TOKEN")
