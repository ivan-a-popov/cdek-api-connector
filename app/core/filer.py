"""TestAPI token YOUR_YADISK_TOKEN"""
import os
import asyncio
import yadisk
from app.core.settings import YADISK_TOKEN
from app.cdek.api.barcode import get_file


async def save_file(url, uuid):
    base_dir = os.path.abspath(os.getcwd())
    await get_file(url, uuid)
    async with yadisk.AsyncClient(token=YADISK_TOKEN, session="httpx") as client:
        r = await client.upload(f"{base_dir}/temp/{uuid}.pdf", f"disk:/TestAPI/{uuid}.pdf", overwrite=True)
        link = await r.get_download_link()
        return link


if __name__ == "__main__":
    asyncio.run(save_file('https://api.edu.cdek.ru/v2/print/barcodes/72753031-ff1b-4879-862d-2585869bcb42.pdf', '72753031-ff1b-4879-862d-2585869bcb42'))
