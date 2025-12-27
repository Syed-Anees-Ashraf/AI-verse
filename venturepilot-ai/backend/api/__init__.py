# API module init
from .onboarding import router as onboarding_router
from .dashboard import router as dashboard_router
from .chat import router as chat_router

__all__ = ["onboarding_router", "dashboard_router", "chat_router"]
