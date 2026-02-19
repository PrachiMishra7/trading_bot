import logging
import os

from flask import Flask, jsonify, request, send_from_directory

from bot.client import BinanceAPIError, BinanceClient
from bot.logging_config import setup_logging
from bot.mock_exchange import start_in_background
from bot.orders import (place_limit_order, place_market_order,
                        place_stop_market_order)

# Setup
setup_logging()
logger = logging.getLogger("trading_bot.server")

app = Flask(__name__)

# Start mock exchange on port 5000 in background
start_in_background()

# Client talks to mock exchange on port 5000
client = BinanceClient()

# Store orders locally for history display
order_history = []


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "No data received."}), 400

    symbol     = str(data.get("symbol", "")).strip().upper()
    side       = str(data.get("side", "")).strip().upper()
    order_type = str(data.get("type", "")).strip().upper()
    quantity   = data.get("quantity")
    price      = data.get("price")
    stop_price = data.get("stopPrice")

    # Validation
    if not symbol:
        return jsonify({"error": "Symbol is required."}), 400
    if side not in ("BUY", "SELL"):
        return jsonify({"error": "Side must be BUY or SELL."}), 400
    if order_type not in ("MARKET", "LIMIT", "STOP_MARKET"):
        return jsonify({"error": "Invalid order type."}), 400
    if not quantity:
        return jsonify({"error": "Quantity is required."}), 400
    if order_type == "LIMIT" and not price:
        return jsonify({"error": "Price is required for LIMIT orders."}), 400
    if order_type == "STOP_MARKET" and not stop_price:
        return jsonify({"error": "Stop price is required for STOP_MARKET orders."}), 400

    logger.info(
        "Web order → %s %s %s qty=%s",
        side, order_type, symbol, quantity
    )

    try:
        if order_type == "MARKET":
            result = place_market_order(
                client, symbol, side, quantity)

        elif order_type == "LIMIT":
            result = place_limit_order(
                client, symbol, side, quantity, price)

        elif order_type == "STOP_MARKET":
            result = place_stop_market_order(
                client, symbol, side, quantity, stop_price)

        # Save to local history
        order_history.append(result)

        logger.info("Order success → orderId=%s", result.get("orderId"))
        return jsonify({"success": True, "order": result})

    except BinanceAPIError as e:
        logger.error("API error %s: %s", e.code, e.message)
        return jsonify({"error": f"API Error {e.code}: {e.message}"}), 400

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(list(reversed(order_history)))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n  Trading Bot Web Server")
    print(f"  Open http://localhost:{port} in your browser\n")
    app.run(host="0.0.0.0", port=port, debug=False)