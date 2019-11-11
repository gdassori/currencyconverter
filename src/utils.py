import functools

from aiohttp.web_exceptions import HTTPBadRequest

from src.exceptions import MicroCurrencyConverterException


def catch_exceptions(fun):
    @functools.wraps(fun)
    async def wrapper(request):
        try:
            return await fun(request)
        except MicroCurrencyConverterException as e:
            raise HTTPBadRequest(body=e.args and e.args[0] or str(e))
    return wrapper
