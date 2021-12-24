import logging
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import requests
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def get_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_dog_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_dog_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def get_image_by_name(by_name: str):
    response = requests.get(
        "https://pixabay.com/api/",
        params={
            "key": "24970643-36536ee8003433f073f9ee97a",
            "q": by_name,
            "image_type": "photo"
        }
    ).json()["hits"]

    return choice(response)["largeImageURL"] if response else "Images not found"


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Input /bob for random dog image or input any world for getting image')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(f"Nice to meet you {update.message.text}")


def find_image(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=get_image_by_name(update.message.text))


@run_async
def bop(update, context):
    url = get_dog_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main():
    updater = Updater('812147190:AAFKnWzeHai_42rNmTKDOtbd-HttxLYrAvU', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, find_image))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()