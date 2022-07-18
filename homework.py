import logging
import os
import sys
import time
from http import HTTPStatus
from pathlib import Path

import requests
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

BASE_DIR = Path(__file__).resolve().parent.parent

"""Задана глобальная конфигурация для всех логгеров"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправляет сообщения."""
    try:
        logging.info(f'Отправляем сообщение в телеграм: {message}')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception:
        raise exceptions.SendMessageException()
    else:
        logger.info(f'Сообщение в чат отправлено: {message}')


def get_api_answer(current_timestamp):
    """Отправляет запрос к API на ENDPOINT."""
    timestamp = current_timestamp or 0
    params = {'from_date': timestamp}
    try:
        logging.info('Начинаем отправку запроса к API')
        answer = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        logger.info('Отправлен запрос к API')
    except Exception:
        raise exceptions.GetAPIException()
    if answer.status_code != HTTPStatus.OK:
        raise exceptions.GetAPIException()
    try:
        return answer.json()
    except ValueError:
        raise ValueError('Ошибка, формат не соответствует json')


def check_response(response):
    """Проверяем полученный API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API отличен от словаря')
    homework = response.get('homeworks')
    logger.info('Получены ваши работы по ключу homeworks')
    if not isinstance(homework, list):
        raise exceptions.IncorrectFormatError('Неверный формат homeworks')
    if homework is None:
        raise IndexError('Список домашних работ пуст')
    return homework


def parse_status(homework):
    """Проверяет статус конкретной домашней работы."""
    if 'homework_name' not in homework:
        raise KeyError('Отсутствует ключ homework_name в ответе API')
    if 'status' not in homework:
        raise Exception('Отсутствует ключ status в ответе API')
    homework_name = homework.get('homework_name')
    logger.info(f'Проверяем вашу работу {homework_name}')
    homework_status = homework.get('status')
    logger.info('Проверяем статус работы')
    if homework_status is None:
        raise IndexError('Статус домашней работы пуст')
    if homework_name is None:
        raise IndexError('Домашняя работа пуста')
    if homework_status not in HOMEWORK_STATUSES:
        raise Exception(f'Неизвестный статус работы: {homework_status}')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет, передались ли все токены корректно."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    status = ''
    error_cache_message = ''

    if not check_tokens():
        """Делается запрос к API."""
        logger.critical('Не передались токены')
        sys.exit('Ошибка в передаче токенов, проверь их содержмое!')

    while True:
        try:
            response = get_api_answer(current_timestamp)
            current_timestamp = response.get('current_date')
            status_homework = parse_status(check_response(response)[0])
            if status_homework != status:
                send_message(bot, status_homework)
                status = status_homework
                logger.debug('В ответе нет новых статусов')
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if message != error_cache_message:
                send_message(bot, message)
                error_cache_message = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s [%(levelname)s] - '
            '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s'
        ),
        handlers=[
            logging.FileHandler(f'{BASE_DIR}/output.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()
