import asyncio
import os

from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from dotenv import load_dotenv, find_dotenv
from middleware.db import DateBaseSession
from common.chat_cmds import client
from database.engine import *

from handlers.user import user_router
from handlers.user_group import user_group
from handlers.admin import admin_router

load_dotenv(find_dotenv())


# ----------------------------------------------------------------------------------

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = Dispatcher()

db.include_router(user_router)
db.include_router(user_group)
db.include_router(admin_router)

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await bot.send_message(chat_id=int(-1002192469164), text=
            f'Привет, я снова с Вами!', message_thread_id=int(811))
    await create_db()

async def on_shutdown(bot):
    print("Бот упал :(")


async def main():
    db.startup.register(on_startup)
    db.shutdown.register(on_shutdown)

    db.update.middleware(DateBaseSession(session_pool = session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=client, scope=types.BotCommandScopeAllPrivateChats()
    )

    await db.start_polling(bot, allowed_updates=db.resolve_used_update_types())


asyncio.run(main())
