from . import start, search

routers = [start.router, search.router]

__all__ = ["routers"]