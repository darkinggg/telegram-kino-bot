from . import start, movie_add, movie_delete, stats, broadcast

routers = [
    start.router,
    movie_add.router,
    movie_delete.router,
    stats.router,
    broadcast.router
]

__all__ = ["routers"]