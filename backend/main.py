from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1.api import api_router
from backend.database import engine, Base
import os

# Create FastAPI application
app = FastAPI(
    title="Avionics Health Monitoring API",
    description="Intelligent Avionics Health Monitoring and Predictive Maintenance Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv(
    "BACKEND_CORS_ORIGINS",
    '["http://localhost:8501", "http://localhost:3000"]'
)
# Parse the string to list if it's a string representation
if isinstance(allowed_origins, str):
    import json
    allowed_origins = json.loads(allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    """
    Application startup event.
    
    This function runs when the application starts up.
    It initializes the database by creating all tables.
    In production, use Alembic migrations instead.
    """
    # Create database tables
    # Note: In production, use Alembic migrations instead
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """
    Root endpoint.
    
    Returns basic information about the API.
    """
    return {
        "message": "Avionics Health Monitoring API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API.
    """
    return {"status": "healthy"}
