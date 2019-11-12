import datetime
import random
import urllib
from unittest import TestCase
import asyncio
import aiohttp
from aiohttp.web import _run_app
import time
from src.app import app
from src.router import prices_service


class TestPriceService(TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.done = None
        self.sut_port = random.randint(30000, 35000)

    async def _check_timeout(self):
        s = time.time()
        while 1:
            if self.done:
                break
            if time.time() - s > 60:
                raise TimeoutError
            await asyncio.sleep(2)

    async def get(self, payload):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                'http://127.0.0.1:{}/convert?{}'.format(
                    self.sut_port,
                    urllib.parse.urlencode(payload)
                )
            )
            if response.status == 200:
                data = await response.json()
            else:
                data = await response.text()
        return data

    async def async_tests(self):
        await self.async_test_mutuable_pair()
        await self.async_test_validations()

    async def async_test_mutuable_pair(self):
        today = datetime.datetime.now() - datetime.timedelta(days=1)
        amount_to_trade = 10
        payload = {
            'amount': amount_to_trade,
            'src_currency': 'EUR',
            'dest_currency': 'USD',
            'reference_date': '{}-{}-{}'.format(today.year, today.month, today.day)
        }
        eur_to_usd = await self.get(payload)
        payload = {
            'amount': eur_to_usd['amount'],
            'src_currency': 'USD',
            'dest_currency': 'EUR',
            'reference_date': '{}-{}-{}'.format(today.year, today.month, today.day)
        }
        usd_to_eur = await self.get(payload)
        amount_traded = int(float(usd_to_eur['amount']))
        self.assertEqual(float(usd_to_eur['amount']), amount_traded)
        self.assertEqual(amount_traded, amount_to_trade)
        self.tmp_executed = True

    async def async_test_validations(self):
        amount_to_trade = 10
        payload = {
            'amount': amount_to_trade,
            'src_currency': 'EUR',
            'dest_currency': 'USD',

        }
        response = await self.get(payload)
        self.assertEqual(response, '400: Missing arguments: reference_date')
        payload.pop('amount')
        response = await self.get(payload)
        self.assertEqual(response, '400: Missing arguments: amount, reference_date')
        payload.pop('dest_currency')
        response = await self.get(payload)
        self.assertEqual(response, '400: Missing arguments: amount, dest_currency, reference_date')
        payload.pop('src_currency')
        response = await self.get(payload)
        self.assertEqual(response, '400: Missing arguments: amount, dest_currency, reference_date, src_currency')
        today = datetime.datetime.now() - datetime.timedelta(days=1)
        payload = {
            'amount': 'ffff',
            'src_currency': 'EUR',
            'dest_currency': 'USD',
            'reference_date': '{}-{}-{}'.format(today.year, today.month, today.day)
        }
        response = await self.get(payload)
        self.assertEqual(response, '400: Argument amount with invalid value: ffff')
        payload['amount'] = 10
        payload['src_currency'] = 'USD'
        response = await self.get(payload)
        self.assertEqual(response, '400: USD USD is not a currency pair')
        payload['src_currency'] = 'EUR'
        payload['reference_date'] = '10/10/2010'
        response = await self.get(payload)
        self.assertEqual(response, '400: Argument reference_date with invalid value: 10/10/2010')
        payload['reference_date'] = '{}-{}-{}'.format(today.year, today.month, today.day)
        payload['src_currency'] = 'EURR'
        response = await self.get(payload)
        self.assertEqual(response, '400: Argument src_currency with invalid value: EURR')
        payload['src_currency'] = 'EUR'
        payload['dest_currency'] = 'EURR'
        response = await self.get(payload)
        self.assertEqual(response, '400: Argument dest_currency with invalid value: EURR')
        self.done = True
        self.validations_executed = True

    async def run_system(self):
        self.loop.create_task(_run_app(app, host='127.0.0.1', port=self.sut_port))
        await prices_service.load(callback=self.async_tests)
        await self._check_timeout()

    def test(self):
        self.loop.run_until_complete(self.run_system())
        self.assertTrue(self.tmp_executed)
        self.assertTrue(self.validations_executed)
