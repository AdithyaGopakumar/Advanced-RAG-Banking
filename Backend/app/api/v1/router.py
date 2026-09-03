"""
API v1 router — aggregates all module routers.

Each module owns its own router. This file just collects
and mounts them under the `/api/v1` prefix.
"""

from fastapi import APIRouter

# import all routers from the differnt modules
from app.modules.system.router import router as system_router

v1_router = APIRouter(prefix="/api/v1")

# ─── Register module routers ───
# ──system router──
v1_router.include_router(system_router)

