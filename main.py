"""Main application file. All the magic starts here."""
from fastapi import FastAPI
import uvicorn
from app.cdek.schemas.delivery import DeliveryOrder


app = FastAPI(title="Delivery Connector API")


@app.get("/api/delivery", tags=["General"])
async def check_delivery():
    """Получение информации о доставке"""
    return {"message": "It works!"}


@app.post("/api/sdek", tags=["CDEK"])
async def create_delivery(body: DeliveryOrder):
    """Создание заказа на доставку СДЭК"""
    # print(body.from_location.fias_guid)
    return {"message": "It works!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
