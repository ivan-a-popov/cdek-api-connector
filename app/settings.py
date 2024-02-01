"""File with settings and configs for the project"""
from sqlalchemy.engine import URL


# connect string for the database:
# "postgresql+asyncpg://app_user:changeme@127.0.0.1:5432/app_db?ssl=disable"
DATABASE_URL = URL.create(
            "postgresql+asyncpg",
            username="app_user",
            password="changeme",
            host="127.0.0.1",
            database="app_db",
            query={"ssl": "disable"},
)

CDEK_URL = "https://api.edu.cdek.ru/v2"
CDEK_ID = "EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI"
CDEK_SECRET = "PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG"
