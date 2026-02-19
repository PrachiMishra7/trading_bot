import random
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

orders = {}
order_counter = 1000

PRICES = {
    "BTCUSDT": 97000.0,
    "ETHUSDT": 3200.0,
    "SOLUSDT": 180.0,
}


def get_price(symbol):
    base = PRICES.get(symbol, 100.0)
    return round(base * random.uniform(0.999, 1.001), 2)


@app.route("/fapi/v1/order", methods=["POST"])
def place_order():
    global order_counter

    data = request.form
    symbol     = data.get("symbol", "BTCUSDT")
    side       = data.get("side", "BUY")
    order_type = data.get("type", "MARKET")
    quantity   = data.get("quantity", "0")
    price      = data.get("price", "0")
    stop_price = data.get("stopPrice", "0")
    tif        = data.get("timeInForce", "GTC")

    order_counter += 1
    order_id  = order_counter
    now       = int(time.time() * 1000)
    avg_price = get_price(symbol)

    if order_type == "MARKET":
        order = {
            "orderId":     order_id,
            "symbol":      symbol,
            "side":        side,
            "type":        order_type,
            "status":      "FILLED",
            "origQty":     quantity,
            "executedQty": quantity,
            "avgPrice":    str(avg_price),
            "price":       "0",
            "stopPrice":   "0",
            "timeInForce": "GTC",
            "updateTime":  now,
        }
    elif order_type == "LIMIT":
        order = {
            "orderId":     order_id,
            "symbol":      symbol,
            "side":        side,
            "type":        order_type,
            "status":      "NEW",
            "origQty":     quantity,
            "executedQty": "0",
            "avgPrice":    "0",
            "price":       price,
            "stopPrice":   "0",
            "timeInForce": tif,
            "updateTime":  now,
        }
    elif order_type == "STOP_MARKET":
        order = {
            "orderId":     order_id,
            "symbol":      symbol,
            "side":        side,
            "type":        order_type,
            "status":      "NEW",
            "origQty":     quantity,
            "executedQty": "0",
            "avgPrice":    "0",
            "price":       "0",
            "stopPrice":   stop_price,
            "timeInForce": "GTC",
            "updateTime":  now,
        }
    else:
        return jsonify({"code": -1100, "msg": f"Unsupported order type: {order_type}"}), 400

    orders[order_id] = order
    print(f"  [MOCK EXCHANGE] {order_type} {side} {quantity} {symbol} → orderId={order_id}")
    return jsonify(order)


@app.route("/fapi/v1/order", methods=["GET"])
def get_order():
    order_id = int(request.args.get("orderId", 0))
    order = orders.get(order_id)
    if not order:
        return jsonify({"code": -2013, "msg": "Order does not exist."}), 404
    return jsonify(order)


@app.route("/fapi/v1/time", methods=["GET"])
def server_time():
    return jsonify({"serverTime": int(time.time() * 1000)})


def run():
    print("  [MOCK EXCHANGE] Starting on http://localhost:5000 ...")
    app.run(port=5000, debug=False, use_reloader=False)


def start_in_background():
    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(1)
    print("  [MOCK EXCHANGE] Ready!\n")