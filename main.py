"""Main application file. The magic starts here."""
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import uvicorn
from app.routers.cdek import cdek_router
from app.routers.general import common_router
from app.cdek.api.auth import ApiService


api = ApiService()
app = FastAPI(title="Delivery Connector API", debug=True)

main_router = APIRouter(prefix="/api")
main_router.include_router(common_router)
main_router.include_router(cdek_router)
app.include_router(main_router)

@app.exception_handler(ValidationError)
async def validation_exception_handler(exc: ValidationError):
    """Handle errors"""
    return JSONResponse({"detail": exc.errors()}, status_code=422)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
