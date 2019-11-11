import asyncio
from aiohttp import web
from src.router import routes, prices_service

BANNER = """
Micro Currency Converter, ver 0.1
"""


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    loop = asyncio.get_event_loop()
    loop.create_task(prices_service.load())
    print(BANNER)
    web.run_app(app)
