
import os
import time
import random
import logging

import requests

BASE_URL = os.environ["XUI_BASE_URL"].rstrip("/")
TOKEN = os.environ["XUI_API_TOKEN"]

MIN_INTERVAL = int(os.getenv("MIN_INTERVAL", "1800"))
MAX_INTERVAL = int(os.getenv("MAX_INTERVAL", "5400"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

URL = f"{BASE_URL}/panel/api/server/restartXrayService"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
})


def restart_xray():
    try:
        response = session.post(
            URL,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        try:
            result = response.json()
        except ValueError:
            logging.error("API вернул не JSON: %s", response.text[:500])
            return

        if result.get("success") is True:
            logging.info("Xray: запрос принят API: %s", result.get("msg", "OK"))
        else:
            logging.error("API сообщил об ошибке: %s", result)

    except requests.RequestException as exc:
        logging.exception("Ошибка HTTP-запроса: %s", exc)


def main():
    logging.info("Xray restart scheduler запущен")
    logging.info("API URL: %s", URL)
    logging.info(
        "Интервал: от %s до %s секунд",
        MIN_INTERVAL,
        MAX_INTERVAL,
    )

    while True:
        delay = random.randint(MIN_INTERVAL, MAX_INTERVAL)

        logging.info(
            "Следующий запрос через %d минут (%d секунд)",
            round(delay / 60),
            delay,
        )

        time.sleep(delay)

        restart_xray()


if __name__ == "__main__":
    main()
