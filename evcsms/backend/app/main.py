import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.db.database import engine, Base
import app.db.models  # ensure models are imported before create_all
from app.scheduler.tasks import start_scheduler, shutdown_scheduler

# Routers
from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicles_router
from app.routers.stations import router as stations_router
from app.routers.chargers import router as chargers_router
from app.routers.bookings import router as bookings_router
from app.routers.sessions import router as sessions_router
from app.routers.payments import router as payments_router
from app.routers.notifications import router as notifications_router
from app.routers.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure SQLite/Postgres tables exist
    Base.metadata.create_all(bind=engine)
    try:
        from seed import seed_database
        seed_database()
    except Exception as e:
        print(f"Auto-seed status: {e}")
    # Start APScheduler daemon
    start_scheduler()
    yield
    # Shutdown
    shutdown_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack EV Charging Station Management System (EVCSMS) with OOSMD architectural design.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development & local Vite & cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers under API_V1_PREFIX
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(vehicles_router, prefix=settings.API_V1_PREFIX)
app.include_router(stations_router, prefix=settings.API_V1_PREFIX)
app.include_router(chargers_router, prefix=settings.API_V1_PREFIX)
app.include_router(bookings_router, prefix=settings.API_V1_PREFIX)
app.include_router(sessions_router, prefix=settings.API_V1_PREFIX)
app.include_router(payments_router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications_router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Candidate paths for built frontend assets
candidate_dirs = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "dist")),
]
frontend_dist = next((d for d in candidate_dirs if os.path.isdir(d)), None)

if frontend_dist:
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str = ""):
        if full_path.startswith(("api/", "docs", "redoc", "openapi.json")):
            return {"detail": "Not Found"}
        target_file = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(target_file):
            return FileResponse(target_file)
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
        return {"detail": "Frontend index.html not found"}
else:
    @app.get("/")
    def root():
        return {
            "system": settings.PROJECT_NAME,
            "status": "online",
            "documentation": "/docs",
            "version": "1.0.0",
            "endpoints": f"{settings.API_V1_PREFIX}"
        }

