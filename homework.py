import logging
import os
import time
from turtle import update

from pprint import pprint
import requests

from dotenv import load_dotenv

load_dotenv()
"""Спрятал токены в .env и получаю его от туда с помощью load_dotenv()
и передаю в веременные"""

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

"""Задана глобальная конфигурация для всех логгеров"""
logging.basicConfig(
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    level=logging.INFO,
    filename='main.log',
    filemode='w'
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# handler = RotatingFileHandler('my_logger.log',
#                               maxBytes=50000000,
#                               backupCount=5
#                               )
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s - %(name)s - %(message)s',
)
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправляет сообщения."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info(f'Сообщение в чат отправлено: {message}')
    except Exception as error:
        logger.error(f'Сбой при отправке сообщения в чат: {error}')


def get_api_answer(current_timestamp):
    """Отправляет запрос к API на ENDPOINT."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(ENDPOINT, headers=HEADERS, params=params)
        pprint(homework_statuses.json())
        logger.info(f'Отправлен запрос к API')
    except Exception as error:
        logger.error(f'Сбой при отправке запроса в API: {error}')


def check_response(response):
    """Проверяем полученный API на корректность."""
    try:
        # response = requests.get(ENDPOINT)
        # print(response.json()['homeworks'])
        homework_list = response.json()['homeworks']
        logger.info(f'Получен корректный API')
        # pprint(homework_list)
    except Exception as error:
        logger.error(f'Полученный API некоректен: {error}')


def parse_status(homework):
    """Проверяет статус конкретной домашней работы."""
    try:
        homework_name = homework['homework_name']
        logger.info(f'Получен ключ homework_name')
    except Exception as error:
        logger.error(f'Ключа homework_name нет: {error}')
    try:
        homework_status = homework['status']
        logger.info(f'Получен ключ status')
    except Exception as error:
        logger.error(f'Ключа status нет: {error}')

    verdict = HOMEWORK_STATUSES['homework_status']
    if 
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


# def check_tokens():
#     """Проверяет, передались ли все токены корректно"""
#     return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


# def main():
#     """Основная логика работы бота."""

#     ...

#     bot = telegram.Bot(token=TELEGRAM_TOKEN)
#     current_timestamp = int(time.time())

#     ...

#     while True:
#         try:
#             response = ...

#             ...

#             current_timestamp = ...
#             time.sleep(RETRY_TIME)

#         except Exception as error:
#             message = f'Сбой в работе программы: {error}'
#             ...
#             time.sleep(RETRY_TIME)
#         else:
#             ...


# if __name__ == '__main__':
#     main()
