import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from handlers import start, register, update_user, admin_handlers, solution
from config.config import load_config, Config
from keyboard.menu import set_main_menu

logger = logging.getLogger(__name__)
config: Config = load_config('.env')


def register_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(update_user.router)
    dp.include_router(register.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(solution.router)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting Bot")
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)

    register_routers(dp)

    await set_main_menu(bot)

    try:
        await bot.delete_webhook()
        await dp.start_polling(bot)
    except Exception as ex:
        await bot.close()
        print(ex)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as ex:
        print(ex)
