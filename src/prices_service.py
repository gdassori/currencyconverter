import asyncio
import typing
import decimal
import xmltodict
import aiohttp
from aiohttp import ClientConnectorError
from aiohttp.web_exceptions import HTTPError

from src import exceptions
from src.abstracts import PricesService


DATA_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'


class PricesServiceImpl(PricesService):
    def __init__(self, data_url: str = DATA_URL):
        self._data = {}
        self._data_url = data_url
        self._supported_currencies = set()
        self._range = [None, None]

    def get_quotes_for_date(self, reference_date: str) -> typing.Dict:
        if not self._data:
            raise exceptions.DataUnavailableException('Data not available')
        try:
            return self._data[reference_date]
        except KeyError:
            raise exceptions.ReferenceDateOutOfRange(
                'Date must be a working day be between %s and %s' % self.get_range()
            )

    def get_range(self):
        return tuple(self._range)

    async def load(self, callback=None):
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(self._data_url, raise_for_status=True)
                data = await response.text()
        except (HTTPError, ConnectionRefusedError, ClientConnectorError):
            raise exceptions.DataUnavailableException
        self._supported_currencies.add('eur')
        _data = xmltodict.parse(data)['gesmes:Envelope']['Cube']['Cube']
        for x in _data:
            res = {}
            for y in x['Cube']:
                res[y['@currency'].lower()] = decimal.Decimal(y['@rate'])
                self._supported_currencies.add(y['@currency'].lower())
            self._data[x['@time']] = res
            self._range[0] = (not self._range[0] or self._range[0] > x['@time']) and x['@time'] or self._range[0]
            self._range[1] = (not self._range[1] or self._range[1] < x['@time']) and x['@time'] or self._range[1]
        if callback:
            loop = asyncio.get_event_loop()
            loop.create_task(callback())

    def is_currency_supported(self, currency: str) -> bool:
        return currency.lower() in self._supported_currencies
