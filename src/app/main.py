from os import path

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from app.api.routes import rates
from app.api.utils.shared import load_required_data
from app.db import database

app = FastAPI()
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logger.info("------API is live------")


@app.on_event("startup")
async def startup():
    await database.connect()
    await load_required_data()  # preload the parent-child regions mapping


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    logging.info("logging from the root logger")
    return {"status": "alive"}


app.include_router(rates.router, prefix="/rates", tags=["rates"])

# to handle api level exceptions
@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
    )
