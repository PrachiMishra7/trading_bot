import argparse
from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(value):
    cleaned = value.strip().upper()
    if not cleaned.isalnum():
        raise argparse.ArgumentTypeError(
            f"Invalid symbol '{value}'. Example: BTCUSDT"
        )
    return cleaned


def validate_side(value):
    upper = value.strip().upper()
    if upper not in VALID_SIDES:
        raise argparse.ArgumentTypeError(
            f"Invalid side '{value}'. Must be BUY or SELL."
        )
    return upper


def validate_order_type(value):
    upper = value.strip().upper()
    if upper not in VALID_TYPES:
        raise argparse.ArgumentTypeError(
            f"Invalid type '{value}'. Must be MARKET, LIMIT or STOP_MARKET."
        )
    return upper


def validate_positive_decimal(value, field="value"):
    try:
        d = Decimal(str(value))
    except InvalidOperation:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not a valid number for {field}."
        )
    if d <= 0:
        raise argparse.ArgumentTypeError(
            f"{field} must be greater than zero. Got: {value}"
        )
    return d


def validate_quantity(value):
    return validate_positive_decimal(value, "quantity")


def validate_price(value):
    return validate_positive_decimal(value, "price")


def validate_stop_price(value):
    return validate_positive_decimal(value, "stop-price")