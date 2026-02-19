import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import requests

logger = logging.getLogger("trading_bot.client")

BASE_URL = "http://localhost:5000"


class BinanceAPIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"API error {code}: {message}")


class BinanceClient:
    def __init__(self, api_key="mock_key", api_secret="mock_secret"):
        self._api_key = api_key
        self._api_secret = api_secret
        self._session = requests.Session()
        self._session.headers.update({"X-MBX-APIKEY": api_key})
        logger.debug("Client ready → %s", BASE_URL)

    def _sign(self, params):
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        sig = hmac.new(
            self._api_secret.encode(),
            query.encode(),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = sig
        return params

    def _request(self, method, endpoint, params=None, signed=False):
        params = params or {}
        if signed:
            params = self._sign(params)

        url = f"{BASE_URL}{endpoint}"
        safe = {k: v for k, v in params.items() if k != "signature"}
        logger.debug("→ %s %s | %s", method, endpoint, safe)

        try:
            if method == "GET":
                resp = self._session.get(url, params=params, timeout=5)
            else:
                resp = self._session.post(url, data=params, timeout=5)
        except requests.ConnectionError:
            logger.error("Cannot connect. Is mock server running?")
            raise
        except requests.Timeout:
            logger.error("Request timed out.")
            raise

        logger.debug("← status=%s | %s", resp.status_code, resp.text[:500])

        data = resp.json()

        if isinstance(data, dict) and data.get("code", 0) not in (0, 200):
            raise BinanceAPIError(data["code"], data.get("msg", "Unknown"))

        resp.raise_for_status()
        return data

    def new_order(self, **kwargs):
        logger.info(
            "Placing %s %s | symbol=%s qty=%s price=%s",
            kwargs.get("side"), kwargs.get("type"),
            kwargs.get("symbol"), kwargs.get("quantity"),
            kwargs.get("price", "N/A"),
        )
        return self._request("POST", "/fapi/v1/order", params=kwargs, signed=True)