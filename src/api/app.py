from fastapi import FastAPI
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute

from core.dependency_injection import Container
from core.settings import get_settings

# from src.api.routes import auth, users
from src.api.v1.routes import get_v1_routers

settings = get_settings()
print(settings.API_PORT)


def create_app() -> FastAPI:
    container = Container()
    fast_api = FastAPI(
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        root_path=settings.ROOT_PATH,
    )
    fast_api.container = container
    fast_api.add_api_route(
        "/health", endpoint=healthCheckRoute(factory=HealthCheckFactory())
    )
    fast_api.include_router(get_v1_routers())

    return fast_api


def create_health_route():
    # Add Health Checks
    health_checks = HealthCheckFactory()
    app.add_api_route(
        "/health", endpoint=healthCheckRoute(factory=health_checks)
    )


app = create_app()
