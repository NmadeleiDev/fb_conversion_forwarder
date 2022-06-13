from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute

class CookieAuthMiddlewareRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)
            return response

        return custom_route_handler
