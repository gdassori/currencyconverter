from aiohttp import web

from src.combinators import AmountCombinator, CurrencyCombinator, ReferenceDateCombinator, validate_payload
from src.prices_service import PricesServiceImpl
from src.utils import catch_exceptions
from src.vo_service import MicroCurrencyConverterVOServiceImpl

routes = web.RouteTableDef()
prices_service = PricesServiceImpl()
vo_service = MicroCurrencyConverterVOServiceImpl(prices_service)


@routes.get('/convert')
@catch_exceptions
@validate_payload(
    amount=AmountCombinator,
    src_currency=CurrencyCombinator,
    dest_currency=CurrencyCombinator,
    reference_date=ReferenceDateCombinator
)
async def hello(request):
    response = await vo_service.get_price_for_pair(
        request.query['amount'],
        request.query['reference_date'],
        request.query['src_currency'],
        request.query['dest_currency']
    )
    return web.json_response(data=response)
