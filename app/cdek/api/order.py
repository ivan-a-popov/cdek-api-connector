"""Модуль взаимодействия с API CDEK"""
import asyncio
from time import sleep
from app.logger import log
from app.cdek.api.auth import ApiAuth
from app.settings import CDEK_URL


auth = ApiAuth()

async def test_usage(api, i):
    """Test function for API auth"""
    try:
        response = await api.make_request("get", f"{CDEK_URL}/location/regions")
    except Exception as e:
        log.error('Error: %s', e)
        return
    log.info((response.json()[i]))

# Run the example usage within an asynchronous context
if __name__ == "__main__":
    for i in range(100):
        asyncio.run(test_usage(auth, i))
        sleep(10)
