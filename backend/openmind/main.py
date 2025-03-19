from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openmind.routes import auth

app = FastAPI(
    title="OpenMind API",
    description="API for OpenMind project",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to OpenMind API"}
