"""
Remzy Care Partner API — Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import (
    auth_router,
    attendance_router,
    leave_router,
    workday_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Remzy Care Partner Workforce API",
)

# CORS — allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

# Register all routers
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(attendance_router, prefix=API_PREFIX)
app.include_router(leave_router, prefix=API_PREFIX)
app.include_router(workday_router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Remzy Care Partner API is running.",
        "version": "1.0.0",
        "docs": "/docs",
    }