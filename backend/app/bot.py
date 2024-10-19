import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from app.config import get_config, Bot


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

bot_token = get_config(Bot, 'bot')
bot = Bot(token=bot_token.token)
dp = Dispatcher(bot)


async def notify_user(telegram_id: str, 
                      message_text: str):

    await bot.send_message(telegram_id, f"Новое сообщение: {message_text}")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Я уведомлю тебя о новых сообщениях, когда ты офлайн.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)