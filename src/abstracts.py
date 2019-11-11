import abc
import typing


class PricesService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def is_currency_supported(self, currency: str) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def is_date_indexed(self, reference_date: str) -> bool:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_quotes_for_date(self, reference_date: str) -> typing.Dict:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def load(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_range(self) -> typing.Tuple[str, str]:
        pass


class MicroCurrencyConverterVOService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_price_for_pair(self, amount: str, reference_date: str, src_currency: str, dest_currency: str):
        pass  # pragma: no cover
