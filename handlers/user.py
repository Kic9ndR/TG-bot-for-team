import os
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, or_f, StateFilter
from aiogram.types import Message
from filter.chat_filters import ChatFilter
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.orm_query import *
from common.chat_cmds import admin

user_router = Router()
user_router.message.filter(ChatFilter(["private"]))


@user_router.message(
    or_f(
        Command("start"), (F.text.lower() == "в начало ↩️"), (F.text.lower() == "старт")
    )
)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer('Привет ебать')


@user_router.message(Command("faq"))
async def FAQ_cmd(message: types.Message):
    print('Отправил вопросы')
    # await message.answer('Пожалуйста, выберите вопрос который Вас беспокоит', reply_markup = await choice_qq_btns())


@user_router.message(Command("add_admin"))
async def add_admins(message: types.Message, bot: Bot, session: AsyncSession) -> None:
    get_admins_list = await orm_get_admins(session)
    admins = []
    admins.append(message.from_user.id)
    # for i in get_admins_list:
    #     admins.append(i.user_id)

    message_id = message.message_id

    # if message.chat.id == int(admin_chat):
    #     admin_id = message.from_user.id
    #     if admin_id not in admins:    
    #         await orm_add_admin(
    #             session, 
    #             user_id = message.from_user.id,
    #             name = message.from_user.first_name,
    #             username = message.from_user.username, 
    #             )
    #         admins.append(admin_id)


    bot.my_admins_list = admins
    print(bot.my_admins_list)
    # if message.from_user.id in admins:
    await message.delete()
    await bot.set_my_commands(
        commands=admin, scope=types.BotCommandScopeAllPrivateChats()
    )
        
    # else:
    #     await message.answer('Ай-ай-ай, Вам сюда нельзя!')
    await message.answer('Добавил админа')