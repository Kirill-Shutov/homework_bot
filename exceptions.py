class GetAPIException(Exception):
    """Исключение для проверки запроса к API."""

    pass

class APIResponseException(Exception):
    """Исключение для проверки ответа API на корректность."""

    pass

class IncorrectFormatError(Exception):
    """Исключение для проверки формата на корректность."""

    pass

class SendMessageException(Exception):
    """Исключение для отправки сообщения."""

    pass