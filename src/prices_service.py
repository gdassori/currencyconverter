import typing
import decimal
import xmltodict
import aiohttp

from src import exceptions
from src.abstracts import PricesService


DATA_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'


class PricesServiceImpl(PricesService):
    def __init__(self, data_url=DATA_URL):
        self._data = {}
        self._data_url = data_url
        self._supported_currencies = {'eur'}
        self._range = [None, None]

    def get_quotes_for_date(self, reference_date: str) -> typing.Dict:
        if not self._data:
            raise exceptions.DataUnavailableException('Data not available')
        return self._data[reference_date]

    def get_range(self):
        return tuple(self._range)

    async def load(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(self._data_url, raise_for_status=True)
            data = await response.text()
        _data = xmltodict.parse(data)['gesmes:Envelope']['Cube']['Cube']
        for x in _data:
            res = {}
            for y in x['Cube']:
                res[y['@currency'].lower()] = decimal.Decimal(y['@rate'])
                self._supported_currencies.add(y['@currency'].lower())
            self._data[x['@time']] = res
            self._range[0] = (not self._range[0] or self._range[0] > x['@time']) and x['@time'] or self._range[0]
            self._range[1] = (not self._range[1] or self._range[1] < x['@time']) and x['@time'] or self._range[1]

    def is_currency_supported(self, currency: str) -> bool:
        return currency.lower() in self._supported_currencies

    def is_date_indexed(self, date: str):
        try:
            quotes = self.get_quotes_for_date(date)
            return bool(quotes)
        except KeyError:
            return False
