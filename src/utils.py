import functools

from aiohttp.web_exceptions import HTTPBadRequest

from src import Logger
from src.exceptions import MicroCurrencyConverterException


def catch_exceptions(fun):
    @functools.wraps(fun)
    async def wrapper(request):
        try:
            return await fun(request)
        except MicroCurrencyConverterException as e:
            Logger.debug('Exception handled')
            raise HTTPBadRequest(reason=e.args and e.args[0] or str(e))
    return wrapper
