"""TestAPI token YOUR_YADISK_TOKEN"""
import os
import asyncio
import yadisk
from app.core.settings import YADISK_TOKEN


async def test():
    base_dir = os.path.abspath(os.getcwd())
    async with yadisk.AsyncClient(token=YADISK_TOKEN, session="httpx") as client:
        print('Проверяем, валиден ли токен')
        print(await client.check_token())
        # print('Получаем информацию о диске')
        # print(await client.get_disk_info())
        print('Загружаем тестовый файл')
        r = await client.upload(f"{base_dir}/temp/file.txt", "disk:/TestAPI/testfile1.txt", overwrite=True)
        link = await r.get_download_link()
        return link
        # print('Содержимое каталога:')
        # print([i async for i in await client.listdir("disk:/TestAPI")])

if __name__ == "__main__":
    asyncio.run(test())
