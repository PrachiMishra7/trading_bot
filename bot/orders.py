import logging

logger = logging.getLogger("trading_bot.orders")


def _clean(raw):
    keys = [
        "orderId", "symbol", "side", "type", "status",
        "origQty", "executedQty", "avgPrice",
        "price", "stopPrice", "timeInForce",
    ]
    return {k: raw[k] for k in keys if k in raw}


def place_market_order(client, symbol, side, quantity):
    raw = client.new_order(
        symbol=symbol, side=side,
        type="MARKET", quantity=str(quantity),
    )
    logger.info("Market order done. orderId=%s avgPrice=%s",
                raw.get("orderId"), raw.get("avgPrice"))
    return _clean(raw)


def place_limit_order(client, symbol, side, quantity, price, tif="GTC"):
    raw = client.new_order(
        symbol=symbol, side=side, type="LIMIT",
        quantity=str(quantity), price=str(price), timeInForce=tif,
    )
    logger.info("Limit order placed. orderId=%s status=%s",
                raw.get("orderId"), raw.get("status"))
    return _clean(raw)


def place_stop_market_order(client, symbol, side, quantity, stop_price):
    raw = client.new_order(
        symbol=symbol, side=side, type="STOP_MARKET",
        quantity=str(quantity), stopPrice=str(stop_price),
    )
    logger.info("Stop-market order placed. orderId=%s",
                raw.get("orderId"))
    return _clean(raw)