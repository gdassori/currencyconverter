import functools
import re

from pycomb import combinators
from pycomb.exceptions import PyCombValidationError

from src import exceptions


def is_amount(amount):
    try:
        return bool(float(amount))
    except ValueError:
        return


CurrencyCombinator = combinators.subtype(
    combinators.String,
    lambda currency: len(currency) == 3
)

ReferenceDateCombinator = combinators.subtype(
    combinators.String,
    lambda date: re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', date)
)

AmountCombinator = combinators.subtype(
    combinators.String,
    is_amount
)


def validate_payload(**rules):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(request):
            valid_args = set(request.query.keys()) & set(rules.keys())
            if valid_args != set(rules.keys()):
                raise exceptions.MissingArgumentsException(
                    'Missing arguments: %s' % ', '.join(sorted(set(rules.keys()) - valid_args))
                )
            for key, validator in rules.items():
                try:
                    validator(request.query[key])
                except PyCombValidationError:
                    raise exceptions.InvalidArgumentException(
                        'Argument %s with invalid value: %s' % (key, request.query[key])
                    )
            return fun(request)
        return wrapper
    return decorator
