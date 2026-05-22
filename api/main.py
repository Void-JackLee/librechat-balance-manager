from fastapi import FastAPI, HTTPException, Request
from . import controller
from .result import err, ok

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, e: HTTPException):
    return err(e.detail, e.status_code)

@app.exception_handler(Exception)
async def general_error_handler(request: Request, e: Exception):
    return err(f"Internal server error: {e}", 500)

app.include_router(controller.app, prefix="/api", tags=["api"])