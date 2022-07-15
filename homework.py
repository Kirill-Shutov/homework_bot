from http import HTTPStatus
import logging
import os
import time
from turtle import update

from pprint import pprint
import requests
from telegram import Bot
import telegram
from dotenv import load_dotenv
import exceptions

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
# logging.basicConfig(
#     format='%(asctime)s, %(levelname)s, %(funcName)s, %(message)s',
#     level=logging.INFO,
#     # filename='main.log',
#     # filemode='w'
#     )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


# def send_message(bot, message):
#     """Отправляет сообщения."""
#     try:
#         bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
#         logger.info(f'Сообщение в чат отправлено: {message}')
#     except Exception as error:
#         logger.error(f'Сбой при отправке сообщения в чат: {error}')


# def get_api_answer(current_timestamp):
#     """Отправляет запрос к API на ENDPOINT."""
#     timestamp = current_timestamp or int(time.time())
#     params = {'from_date': timestamp}
#     try:
#         answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
#         logger.info(f'Отправлен запрос к API')
#     except Exception as error:
#         logger.error(f'Сбой при отправке запроса в API: {error}')
#         raise exceptions.GetAPIException
#     if answer.status_code != HTTPStatus.OK:
#         logger.error(f'Сбой при запросе к эндпоинту')
#         raise exceptions.GetAPIException()
#     return answer.json()

def check_response(response):
    """Проверяем полученный API на корректность."""
    try:
        response = requests.get(ENDPOINT)
        homework_list = response('homeworks')
        logger.info(f'Получен корректный API: {homework_list}')
    except Exception as error:
        logger.error(f'Полученный API некорректен: {error}')


# def parse_status(homework):
#     """Проверяет статус конкретной домашней работы."""
#     try:
#         homework_name = homework['homework_name']
#         logger.info(f'Получен ключ: {homework_name}')
#     except Exception as error:
#         logger.error(f'Ключа homework_name нет: {error}')
#     try:
#         homework_status = homework['status']
#         logger.info(f'Получен ключ: {homework_status}')
#     except Exception as error:
#         logger.error(f'Ключа status нет: {error}')

#     verdict = HOMEWORK_STATUSES['homework_status']
#     if verdict is None:
#         logger.error(f'Неизвестный статус домашки')
#     return f'Изменился статус проверки работы "{homework_name}". {verdict}'


# def check_tokens():
#     """Проверяет, передались ли все токены корректно"""
#     return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    """Делается запрос к API."""
    # if not check_tokens():
    # logger.critical(f'Не передались токены')

    response = requests.get(ENDPOINT)
    check_response(response)
    
    """Проверяем полученный API на корректность."""
    # bot = telegram.Bot(token=TELEGRAM_TOKEN)
    # current_timestamp = int(time.time())
    # status = ''
    # error_cache_message = ''

    # while True:
    #     """Проверка ответа"""
    #     try:
    #         response = get_api_answer(current_timestamp)
    #         current_timestamp = response.get('current_date') 
    #         status_homework = parse_status(check_response(response)) 
    #         if status_homework != status: 
    #             send_message(bot, status_homework) 
    #             status = status_homework 
    #         time.sleep(RETRY_TIME)
    #     except Exception as error:
    #         message = f'Сбой в работе программы: {error}'
    #         # logger.error(error) 
    #         logger.error(message)
    #         # message_t = str(error)            
    #         if message != error_cache_message: 
    #             send_message(bot, message) 
    #             error_cache_message = message
    #     time.sleep(RETRY_TIME)

if __name__ == '__main__':
    main()

    #         current_timestamp = response['current_date']
    #         time.sleep(RETRY_TIME)

    #     except Exception as error:
    #         message = f'Сбой в работе программы: {error}'
    #         ...
    #         time.sleep(RETRY_TIME)
    #     else:
    #         ...


