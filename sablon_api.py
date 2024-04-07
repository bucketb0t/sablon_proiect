"""
Sablon Management API

This module defines a FastAPI application for managing Sablon documents. It includes routing for CRUD operations on Sablon documents.

Usage:
    To start the server, run this script directly. The server listens on port 8000 by default.

Attributes:
    None

Functions:
    None
"""

import uvicorn
from fastapi import FastAPI

from routes.sablon_routes import router as sablon_router

app = FastAPI()
app.include_router(sablon_router, prefix="/sablon", tags=["sabloane"])

if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000
        )
    except KeyboardInterrupt:
        print("Server is shutting down...")
