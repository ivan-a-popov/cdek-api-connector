"""Класс, обеспечивающий авторизацию и обновление токена, 
а также подготовку авторизованного запроса
"""
from datetime import datetime, timedelta
import httpx
from app.settings import CDEK_URL, CDEK_ID, CDEK_SECRET
from app.logger import log


class ApiService:
    """Класс (singleton), обеспечивающий авторизацию и обновление токена"""
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ApiService, cls).__new__(cls)
            cls._instance.token = None
            cls._instance.token_expiration = None
        return cls._instance

    async def get_token(self):
        """Проверка валидности токена"""
        if not self.token or datetime.utcnow() > self.token_expiration:
            log.info('refreshing CDEK autorization token')
            try:
                await self.refresh_token()
            except Exception as e:
                log.critical("Error refreshing token: %s", e)
        return self.token

    async def refresh_token(self):
        """Получение нового токена"""
        token_url = f"{CDEK_URL}/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        params = {
            "grant_type": "client_credentials",
            "client_id": CDEK_ID,
            "client_secret": CDEK_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, headers=headers, data=params)

            log.info("Response: %s - %s", response.status_code, response.text)

            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data["access_token"]
                expiration_seconds = token_data["expires_in"]
                self.token_expiration = datetime.utcnow() + timedelta(seconds=expiration_seconds)
            else:
                log.critical(response.text)
                raise Exception(f"Failed to refresh token. Status code: {response.status_code}")

async def make_request(api, method, url, **kwargs):
    """Get the token and add Authorization header to the request"""
    token = await api.get_token()
    headers = kwargs.setdefault("headers", {})
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        return await client.request(method, url, **kwargs)
