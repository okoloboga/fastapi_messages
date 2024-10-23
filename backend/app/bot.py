import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from app.config import get_config, Bot as BotConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Получаем конфигурацию для бота, которая содержит токен из файла конфигурации.
bot_token = get_config(BotConfig, 'bot')

# Создаем экземпляр бота, используя полученный токен.
bot = Bot(token=bot_token.token)

# Создаем экземпляр диспетчера с использованием памяти для хранения данных.
dp = Dispatcher(storage=MemoryStorage())

# Создаем роутер для обработки команд и сообщений.
router = Router()


# Обработчик команды "/start".
# Отправляет приветственное сообщение, когда пользователь вводит команду /start.
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Я уведомлю тебя о новых сообщениях, когда ты офлайн.")


# Асинхронная функция для уведомления пользователя.
# Отправляет сообщение пользователю с указанным telegram_id.
async def notify_user(telegram_id: str, message_text: str):
    await bot.send_message(telegram_id, f"Новое сообщение: {message_text}")


# Основная функция для запуска бота.
# Включает роутер в диспетчер и начинает опрос обновлений.
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


# Точка входа для запуска бота.
if __name__ == '__main__':
    asyncio.run(main())
