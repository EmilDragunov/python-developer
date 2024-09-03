import os
import time
import requests
from dotenv import load_dotenv
from telebot import TeleBot, apihelper
import logging
import sys
from datetime import datetime, timedelta
from http import HTTPStatus
from json import JSONDecodeError
import message as m

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка наличия токенов."""
    missing_tokens = []
    for token_name in (
        'PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID'
    ):
        if not globals()[token_name]:
            missing_tokens.append(token_name)
    if missing_tokens:
        logging.critical(m.ERROR_MISSING_TOKENS.format(
            missing_tokens=', '.join(missing_tokens)
        ))
        raise ValueError(m.ERROR_MISSING_TOKENS.format(
            missing_tokens=', '.join(missing_tokens)
        ))


def send_message(bot, message):
    """Отправка сообщения в Telegram."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug(m.BOT_OK.format(message))
    except apihelper.ApiTelegramException as error:
        raise ConnectionError(m.BOT_ERROR.format(error)) from error


def get_api_answer(timestamp):
    """Обращение к API."""
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            url=ENDPOINT, headers=HEADERS, params=payload
        )
    except requests.RequestException as error:
        message = m.API_ERROR1.format(
            ENDPOINT, HEADERS, payload, error
        )
        raise ConnectionError(message) from error

    if homework_statuses.status_code != HTTPStatus.OK:
        raise ConnectionError(
            m.API_ERROR.format(homework_statuses.status_code)
        )
    try:
        return homework_statuses.json()
    except JSONDecodeError as error:
        raise ConnectionRefusedError(
            m.JSON_ERROR.format(error)
        ) from error


def check_response(response):
    """Проверяет ответ API."""
    if not isinstance(response, dict):
        raise TypeError(m.NO_DICT.format(type(response)))
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError(m.NO_LIST.format(type(homeworks)))
    if not homeworks:
        raise TypeError(m.NO_INFO)
    return homeworks[0]


def parse_status(homework):
    """Обработка статуса домашней работы."""
    try:
        homework_name = homework.get('homework_name')
        if not homework.get('homework_name'):
            raise ValueError(m.API_ERROR2)
        verdict = HOMEWORK_VERDICTS[homework.get('status')]
        return m.STATUS_MESSAGE.format(homework_name, verdict)
    except KeyError:
        raise KeyError(m.NOT_STATUS)


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int((datetime.now() - timedelta(days=30)).timestamp())
    status = None
    last_error_message = None
    while True:
        try:
            answer_api = check_response(get_api_answer(timestamp))
            if status != answer_api.get('status'):
                send_message(bot, parse_status(answer_api))
                logging.debug(m.STATUS_CHANGED)
            status = answer_api.get('status')
        except Exception as error:
            error_message = m.ERROR_MESSAGE.format(error)
            logging.error(error_message)
            if str(error) != str(last_error_message):
                send_message(bot, error_message)
            last_error_message = error
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '(%(filename)s -> %(funcName)s -> %(lineno)s)'
            '%(asctime)s, %(name)s: %(levelname)s - %(message)s'
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                filename=__file__ + '.log', mode='w', encoding='utf-8'
            ),
        ],
    )
    main()
