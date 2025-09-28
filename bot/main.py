import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from environs import Env
from redis.asyncio import Redis
from src.dialogs.dialog import tasks_dialog
from src.handlers.menu import router as menu
from src.webhook import start_webhook_server

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")

REDIS_HOST = env("REDIS_HOST", "redis")

redis = Redis(host=REDIS_HOST, port=6379, db=0)
storage = RedisStorage(redis=redis)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp = Dispatcher()

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    dp.include_router(menu)
    dp.include_router(tasks_dialog)

    setup_dialogs(dp)
    asyncio.create_task(start_webhook_server(bot))

    await bot.set_my_commands(
        [BotCommand(command="start", description="Стартовое меню")]
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
