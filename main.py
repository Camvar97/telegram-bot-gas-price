import requests
import logging
import os
import random
import sys

import datetime as dt

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler


# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def get_msg():
    url = 'https://www.680news.com/toronto-gta-gas-prices/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    parent = soup.find('table', {'class': 'tg'}).find_all('tr')
    today = parent[1].find_all('td')

    date = dt.datetime.strptime(today[0].text, '%m/%d/%Y')
    date = date + dt.timedelta(days=1)
    date = date.strftime("%m/%d/%Y")
    change = today[1].text
    value = today[2].text
    middle = change[0]

    if middle == '-':
        middle = 'will drop {} to {}'.format(change[1:], value)
    elif middle == '+':
        middle = 'will rise {} to {}'.format(change[1:], value)
    else:
        middle = 'wont change and stay at {}'.format(value)

    msg = 'The price of gas on {} {}'.format(date, middle)
    return msg


def start_handler(bot, update):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text(
        "Hello from Canada!\nThis bot will return the price changes for Toronto and the GTA\nPress /get_price to get the price change")


def get_price_handler(bot, update):
    # Creating a handler-function for /random command
    number = random.randint(0, 10)
    logger.info("User {} got gas prices".format(
        update.effective_user["id"], number))
    update.message.reply_text(get_msg())


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(
        CommandHandler("get_price", get_price_handler))

    run(updater)
