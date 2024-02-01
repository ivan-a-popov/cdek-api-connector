"""Main application file. All the magic starts here."""
from fastapi import FastAPI, APIRouter
import uvicorn
from app.routers.cdek import cdek_router
from app.routers.common import common_router


app = FastAPI(title="Delivery Connector API")
main_router = APIRouter(prefix="/api")
main_router.include_router(common_router)
main_router.include_router(cdek_router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
