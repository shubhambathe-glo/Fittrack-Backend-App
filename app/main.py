# ==================== Main FastAPI App ====================
# File: app/main.py

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
import logging

from app.core.config import settings
from app.api.v1.routes import admin, auth, users, workouts, goals, measurements, tenants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Cloud-native fitness tracking application with microservices architecture",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ==================== CORS Middleware ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Request Logging Middleware ====================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests with timing
    """
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Time: {process_time:.4f}s"
    )
    
    return response


# ==================== Exception Handlers ====================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with custom response format
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle database errors
    """
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "message": "Database error occurred"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all other exceptions
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "message": "An unexpected error occurred"
        }
    )


# ==================== Health Check ====================
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        },
        "message": "Service is healthy"
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    """
    return {
        "success": True,
        "data": {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs_url": "/docs",
            "health_url": "/health"
        },
        "message": "Welcome to Fitness Tracking API"
    }


# ==================== Include Routers ====================

# Admin routes
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)

# Auth routes (no prefix needed, already has /auth)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

# User routes
app.include_router(users.router, prefix=settings.API_V1_PREFIX)

# Workout routes
app.include_router(workouts.router, prefix=settings.API_V1_PREFIX)

# Goal routes
app.include_router(goals.router, prefix=settings.API_V1_PREFIX)

# Measurement routes
app.include_router(measurements.router, prefix=settings.API_V1_PREFIX)

# Tenant routes (admin only)
app.include_router(tenants.router, prefix=settings.API_V1_PREFIX)


# ==================== Startup & Shutdown Events ====================
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # You can add database connection check here
    # You can add Redis connection check here
    # You can add other initialization logic here


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    logger.info(f"Shutting down {settings.APP_NAME}")
    # Clean up resources here if needed
    