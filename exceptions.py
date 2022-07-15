class GetAPIException(Exception):
    """Исключение для проверки запроса к API."""

    pass

class APIResponseException(Exception):
    """Исключение для проверки ответа API на корректность."""

    pass
