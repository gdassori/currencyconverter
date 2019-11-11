import random
from unittest import TestCase
import asyncio

import os
from aiohttp import web
from aiohttp.web import _run_app

from src import exceptions
from src.prices_service import PricesServiceImpl


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TestPriceService(TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.test_webserver_port = random.randint(30000, 35000)
        self.sut = PricesServiceImpl(data_url='http://127.0.0.1:{}'.format(self.test_webserver_port))

    def run_webserver(self):
        async def response(*a):
            with open(__location__ + '/fixtures/eurofxref-hist-90d.xml') as f:
                x = f.read()
            return web.Response(text=x, content_type="text/xml")

        self.app = web.Application()
        self.app.add_routes([web.get('/', response)])
        self.loop.create_task(_run_app(self.app, host='127.0.0.1', port=self.test_webserver_port))

    async def async_test(self):
        with self.assertRaises(exceptions.DataUnavailableException):
            await self.sut.load()
        self.run_webserver()
        with self.assertRaises(exceptions.DataUnavailableException):
            self.sut.get_quotes_for_date('2020-10-10')
        await self.sut.load()
        with self.assertRaises(exceptions.ReferenceDateOutOfRange):
            self.sut.get_quotes_for_date('2020-10-10')
        self.assertTrue(self.sut.get_quotes_for_date('2019-11-11'))

    def test(self):
        self.loop.run_until_complete(self.async_test())
