"""
Authentication dependencies.

Use these as FastAPI dependencies on routes or routers that need auth.
Routes without these dependencies are public.

Usage:
    # Single route
    @router.get("/protected", dependencies=[Depends(require_auth)])

    # Entire router
    router = APIRouter(dependencies=[Depends(require_auth)])

    # Admin-only route
    @router.delete("/users/{id}", dependencies=[Depends(require_admin)])
"""

import logging

from fastapi import Request

from app.core.exceptions import UnauthorizedException, ForbiddenException

logger = logging.getLogger(__name__)


async def require_auth(request: Request) -> None:
    """
    Dependency: ensures the request is authenticated.

    Apply to any route or router that requires a logged-in user.
    Currently a passthrough — replace with real JWT / OAuth2 validation.

    Raises:
        UnauthorizedException: if authentication fails.
    """
    # TODO: Implement real authentication
    # token = request.headers.get("Authorization")
    # if not token:
    #     raise UnauthorizedException("Missing Authorization header")
    # user = validate_jwt(token)
    # request.state.user = user
    pass


async def require_admin(request: Request) -> None:
    """
    Dependency: ensures the request is from an admin user.

    Apply to admin-only routes. Calls require_auth internally
    once real auth is implemented.

    Raises:
        UnauthorizedException: if not authenticated.
        ForbiddenException: if authenticated but not an admin.
    """
    # TODO: Implement real admin check
    # await require_auth(request)
    # if not request.state.user.is_admin:
    #     raise ForbiddenException("Admin access required")
    pass
