import argparse
import os
import sys

from bot.client import BinanceAPIError, BinanceClient
from bot.logging_config import setup_logging
from bot.mock_exchange import start_in_background
from bot.orders import (place_limit_order, place_market_order,
                        place_stop_market_order)
from bot.validators import (validate_order_type, validate_price,
                             validate_quantity, validate_side,
                             validate_stop_price, validate_symbol)


def print_summary(args):
    print("\n" + "─" * 55)
    print("  ORDER REQUEST SUMMARY")
    print("─" * 55)
    print(f"  Symbol    : {args.symbol}")
    print(f"  Side      : {args.side}")
    print(f"  Type      : {args.type}")
    print(f"  Quantity  : {args.quantity}")
    if args.type == "LIMIT":
        print(f"  Price     : {args.price}")
    if args.type == "STOP_MARKET":
        print(f"  Stop Price: {args.stop_price}")
    print("─" * 55)


def print_response(result):
    print("  ORDER RESPONSE")
    print("─" * 55)
    labels = {
        "orderId":     "Order ID",
        "status":      "Status",
        "symbol":      "Symbol",
        "side":        "Side",
        "type":        "Type",
        "origQty":     "Orig Qty",
        "executedQty": "Executed Qty",
        "avgPrice":    "Avg Price",
        "price":       "Limit Price",
        "stopPrice":   "Stop Price",
        "timeInForce": "Time In Force",
    }
    for key, label in labels.items():
        val = result.get(key)
        if val and val not in ("0", "0.00000000"):
            print(f"  {label:<14}: {val}")
    print("─" * 55 + "\n")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Trading Bot — Mock Exchange",
    )
    parser.add_argument("--symbol",        required=True, type=validate_symbol)
    parser.add_argument("--side",          required=True, type=validate_side)
    parser.add_argument("--type",          required=True, type=validate_order_type)
    parser.add_argument("--quantity",      required=True, type=validate_quantity)
    parser.add_argument("--price",         default=None,  type=validate_price)
    parser.add_argument("--stop-price",    default=None,  type=validate_stop_price)
    parser.add_argument("--time-in-force", default="GTC", choices=["GTC", "IOC", "FOK"])
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    logger = setup_logging()

    if args.type == "LIMIT" and not args.price:
        parser.error("--price is required for LIMIT orders.")
    if args.type == "STOP_MARKET" and not args.stop_price:
        parser.error("--stop-price is required for STOP_MARKET orders.")

    start_in_background()

    print_summary(args)

    client = BinanceClient()

    try:
        if args.type == "MARKET":
            result = place_market_order(
                client, args.symbol, args.side, args.quantity)

        elif args.type == "LIMIT":
            result = place_limit_order(
                client, args.symbol, args.side,
                args.quantity, args.price, args.time_in_force)

        elif args.type == "STOP_MARKET":
            result = place_stop_market_order(
                client, args.symbol, args.side,
                args.quantity, args.stop_price)

    except BinanceAPIError as e:
        logger.error("Order failed — code=%s msg=%s", e.code, e.message)
        print(f"\n  ✗ FAILED — Error {e.code}: {e.message}\n")
        sys.exit(1)

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print(f"\n  ✗ FAILED — {e}\n")
        sys.exit(1)

    print_response(result)
    print(f"  ✓ Success! orderId = {result.get('orderId')}\n")


if __name__ == "__main__":
    main()

