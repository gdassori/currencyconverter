import random
from unittest import TestCase
import asyncio

import os

import time

import decimal
from aiohttp import web
from aiohttp.web import _run_app
from src.prices_service import PricesServiceImpl
from src.vo_service import MicroCurrencyConverterVOServiceImpl

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TestPriceService(TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.test_webserver_port = random.randint(30000, 35000)
        self.prices_service = PricesServiceImpl(data_url='http://127.0.0.1:{}'.format(self.test_webserver_port))
        self.sut = MicroCurrencyConverterVOServiceImpl(self.prices_service)
        self.done = False
        self.matched = 0

    async def _check_timeout(self):
        s = time.time()
        while 1:
            if self.done:
                break
            if time.time() - s > 60:
                raise TimeoutError
            await asyncio.sleep(2)

    def run_webserver(self):
        async def response(*a):
            with open(__location__ + '/fixtures/eurofxref-hist-90d.xml') as f:
                x = f.read()
            return web.Response(text=x, content_type="text/xml")

        self.app = web.Application()
        self.app.add_routes([web.get('/', response)])
        self.loop.create_task(_run_app(self.app, host='127.0.0.1', port=self.test_webserver_port))
        self.loop.create_task(self.prices_service.load(callback=self.async_test))

    async def async_test(self):
        self.expected = [
            ["USD", "1.1041"],
            ["JPY", "120.29"],
            ["BGN", "1.9558"],
            ["CZK", "25.51"],
            ["DKK", "7.4722"],
            ["GBP", "0.85743"],
            ["HUF", "334.35"],
            ["PLN", "4.2737"],
            ["RON", "4.7643"],
            ["SEK", "10.7085"],
            ["CHF", "1.0972"],
            ["ISK", "137.7"],
            ["NOK", "10.091"],
            ["HRK", "7.4391"],
            ["RUB", "70.5319"],
            ["TRY", "6.3722"],
            ["AUD", "1.6105"],
            ["BRL", "4.5949"],
            ["CAD", "1.4607"],
            ["CNY", "7.7404"],
            ["HKD", "8.6422"],
            ["IDR", "15540.68"],
            ["ILS", "3.8591"],
            ["INR", "78.9905"],
            ["KRW", "1288"],
            ["MXN", "21.1057"],
            ["MYR", "4.5749"],
            ["NZD", "1.7348"],
            ["PHP", "56.138"],
            ["SGD", "1.5025"],
            ["THB", "33.493"],
            ["ZAR", "16.415"]
        ]
        for x in self.expected:
            price = await self.sut.get_price_for_pair(
                "1", '2019-11-11', 'EUR', x[0]
            )
            self.assertEqual(price['amount'], '{:.2f}'.format(decimal.Decimal(x[1])))
            self.matched += 1
        self.done = True

    def test(self):
        self.run_webserver()
        self.loop.run_until_complete(self._check_timeout())
        self.assertEqual(len(self.expected), self.matched)
