import asyncio
from aiohttp import web
from src.router import routes, prices_service

app = web.Application()
app.add_routes(routes)

BANNER = """
Micro Currency Converter, ver 0.1
"""


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(prices_service.load())
    print(BANNER)
    web.run_app(app)
