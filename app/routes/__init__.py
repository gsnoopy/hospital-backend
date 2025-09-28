from .user_routes import router as user_router
from .auth_routes import router as auth_router

__all__ = ["user_router", "auth_router"]