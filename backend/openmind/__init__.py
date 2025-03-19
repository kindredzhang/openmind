import base64
import os
import random
from pathlib import Path
from typing import Optional

import typer
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openmind.routes import auth, models
from typing_extensions import Annotated

app = typer.Typer()

api_app = FastAPI(
    title="OpenMind API",
    description="API for OpenMind project",
    version="0.1.0",
)

# Configure CORS
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
api_app.include_router(auth.router, prefix="/auth", tags=["auth"])
api_app.include_router(models.router, prefix="/models", tags=["models"])

@api_app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to OpenMind API"}

KEY_FILE = Path.cwd() / ".webui_secret_key"


def version_callback(value: bool):
    if value:
        from openmind.env import VERSION

        typer.echo(f"OpenMind version: {VERSION}")
        raise typer.Exit()

@app.command()
def serve(
    host: str = "0.0.0.0",
    port: int = 8886,
):
    uvicorn.run(api_app, host=host, port=port, forwarded_allow_ips="*")


@app.command()
def dev(
    host: str = "0.0.0.0",
    port: int = 8886,
    reload: bool = True,
):
    uvicorn.run(
        "openmind:api_app",
        host=host,
        port=port,
        reload=reload,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    app()
