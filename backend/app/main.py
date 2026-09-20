from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.admin import (
    router as admin_router,
)
from app.api.routes.analytics import (
    router as analytics_router,
)
from app.api.routes.auth import (
    router as auth_router,
)
from app.api.routes.chat import (
    router as chat_router,
)
from app.api.routes.diet import (
    router as diet_router,
)
from app.api.routes.dietician import (
    router as dietician_router,
)
from app.api.routes.gym_trainer import (
    router as gym_trainer_router,
)
from app.api.routes.habits import (
    router as habits_router,
)
from app.api.routes.iot import (
    router as iot_router,
)
from app.api.routes.nutrition import (
    router as nutrition_router,
)
from app.api.routes.performance import (
    router as performance_router,
)
from app.api.routes.recommendations import (
    router as recommendations_router,
)
from app.api.routes.workouts import (
    router as workouts_router,
)
from app.core.config import settings
from app.services.iot.manager import iot_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown resources."""

    # Render does not provide the local MQTT broker used by a physical Smart
    # Gym setup.  Keeping this optional lets the fitness, camera, and account
    # features start normally in the cloud while retaining MQTT support for
    # local hardware deployments.
    if settings.mqtt_enabled:
        iot_manager.start()

    try:
        yield
    finally:
        if settings.mqtt_enabled:
            iot_manager.stop()


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered fitness management "
        "and assistance platform"
    ),
    version=settings.app_version,
    lifespan=lifespan,
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    gym_trainer_router,
)

app.include_router(
    performance_router,
)

app.include_router(
    workouts_router,
)

app.include_router(
    nutrition_router,
)

app.include_router(
    diet_router,
)

app.include_router(
    dietician_router,
)

app.include_router(
    habits_router,
)

app.include_router(
    recommendations_router,
)

app.include_router(
    chat_router,
)

app.include_router(
    iot_router,
)

app.include_router(
    analytics_router,
)

app.include_router(
    admin_router,
)


@app.get("/")
async def root():
    return {
        "message": (
            "AI Gym & Fitness Assistant "
            "API is running"
        ),
        "status": "healthy",
        "version": settings.app_version,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": (
            "development"
            if settings.debug
            else "production"
        ),
    }
