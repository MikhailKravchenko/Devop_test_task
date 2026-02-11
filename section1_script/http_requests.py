import logging
import sys
from typing import List

import requests


BASE_URL = "https://httpstat.us"

STATUS_CODES: List[int] = [100, 200, 302, 404, 500]


def configure_logging() -> None:
    """Базовая настройка логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def handle_response(url: str, status_code: int, body: str) -> None:
    """
    Обработка HTTP-ответа в соответствии с требованиями задания.

    - 1xx, 2xx, 3xx — логируем статус-код и тело ответа.
    - 4xx, 5xx — генерируем исключение.
    """
    if 100 <= status_code < 400:
        logging.info(
            "Успешный/информационный/редирект-ответ от %s: status=%s, body=%s",
            url,
            status_code,
            body.strip(),
        )
    elif 400 <= status_code < 600:
        raise RuntimeError(
            f"Получен ошибочный HTTP-статус {status_code} от {url}. "
            f"Тело ответа: {body.strip()}"
        )
    else:
        raise RuntimeError(
            f"Получен непредвиденный HTTP-статус {status_code} от {url}. "
            f"Тело ответа: {body.strip()}"
        )


def make_requests() -> None:
    """Выполнить набор HTTP-запросов и обработать ответы."""
    session = requests.Session()

    for code in STATUS_CODES:
        url = f"{BASE_URL}/{code}"
        logging.info("Выполняю запрос к %s", url)

        try:
            response = session.get(url, timeout=10)
        except Exception as exc:
            logging.error("Ошибка при выполнении запроса к %s: %s", url, exc)
            raise

        handle_response(url, response.status_code, response.text)


def main() -> int:
    """Точка входа в скрипт."""
    configure_logging()

    try:
        make_requests()
    except Exception:
        logging.exception("Скрипт завершился с ошибкой.")
        return 1

    logging.info("Скрипт успешно завершил обработку всех запросов.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

