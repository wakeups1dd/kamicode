"""
KamiCode — FastAPI Application

Main application factory with middleware, routes, and health check.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.core.websocket import manager

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: startup and shutdown hooks."""
    # ─── Startup ───────────────────────────────────────────────────
    print(f"KamiCode API starting in {settings.ENVIRONMENT} mode")
    yield
    # ─── Shutdown ──────────────────────────────────────────────────
    print("KamiCode API shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="KamiCode API",
        description=(
            "AI-Native Competitive Programming Platform — "
            "Depth + Speed → Verifiable On-Chain Credentials"
        ),
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ─── CORS Middleware ───────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─── API Routes ────────────────────────────────────────────────
    application.include_router(v1_router, prefix="/api/v1")

    @application.get(
        "/health",
        tags=["System"],
        summary="Health check",
        description="Returns the current health status of the API.",
    )
    async def health_check():
        return {
            "status": "ok",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @application.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    return application


# Application instance used by Uvicorn
app = create_app()
