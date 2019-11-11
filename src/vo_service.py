import decimal

from src import exceptions
from src.abstracts import PricesService, MicroCurrencyConverterVOService


class MicroCurrencyConverterVOServiceImpl(MicroCurrencyConverterVOService):
    def __init__(self, prices_service: PricesService):
        self._prices_services = prices_service

    async def get_price_for_pair(
            self, amount: decimal.Decimal, reference_date: str, src_currency: str, dest_currency: str
    ):
        if not amount:
            raise exceptions.AmountMustBePositiveInteger()
        if not self._prices_services.is_date_indexed(reference_date):
            raise exceptions.ReferenceDateOutOfRange(
                'Date must a working day be between %s and %s' % self._prices_services.get_range()
            )
        if src_currency == dest_currency:
            raise exceptions.InvalidCurrencyPair(
                '%s %s is not a currency pair' % (src_currency, dest_currency)
            )
        eur_conversion = False
        currencies = [src_currency.lower(), dest_currency.lower()]
        for x in currencies:
            eur_conversion = eur_conversion or x == 'eur'
            if not self._prices_services.is_currency_supported(x):
                raise exceptions.CurrencyNotSupportedException('Currency not supported: %s' % x)
        if not eur_conversion:
            raise exceptions.ConversionNotSupportedException('EUR currency must be in the currencies pair')
        currencies.remove('eur')
        reference_date_quotes = self._prices_services.get_quotes_for_date(reference_date)
        quote = reference_date_quotes[currencies[0]]
        if src_currency.lower() == currencies[0]:
            amount = (1 / decimal.Decimal(quote)) * decimal.Decimal(amount)
        else:
            amount = (decimal.Decimal(quote) / 1) * decimal.Decimal(amount)
        return {
            "amount": "{:.2f}".format(amount),
            "currency": dest_currency
        }
