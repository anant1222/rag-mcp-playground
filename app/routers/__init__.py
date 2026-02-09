"""Routers module"""

from app.routers.index import router, register_routers
from app.routers import rag

__all__ = ["router", "register_routers", "rag"]
