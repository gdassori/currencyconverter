class MicroCurrencyConverterException(BaseException):
    pass


class CurrencyNotSupportedException(MicroCurrencyConverterException):
    pass


class ReferenceDateOutOfRange(MicroCurrencyConverterException):
    pass


class ConversionNotSupportedException(MicroCurrencyConverterException):
    pass


class InvalidCurrencyPair(MicroCurrencyConverterException):
    pass


class DataUnavailableException(MicroCurrencyConverterException):
    pass


class MissingArgumentsException(MicroCurrencyConverterException):
    pass


class InvalidArgumentException(MicroCurrencyConverterException):
    pass
