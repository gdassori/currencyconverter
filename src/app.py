import asyncio
from aiohttp import web
from src.router import routes, prices_service

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    loop = asyncio.get_event_loop()
    loop.create_task(prices_service.load())
    web.run_app(app)
