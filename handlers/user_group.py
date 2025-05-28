import asyncio
import os
from sre_parse import State
from aiogram import F, Bot, types, Router
from aiogram.filters import Command, StateFilter, or_f
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filter.chat_filters import ChatFilter
from kbrd.inline import *


user_group = Router()
user_group.message.filter(ChatFilter(['group', 'supergroup']))

USER_CHAT=-1002192469164

#______________________________________________________________________________________________________________________________________
async def del_inline_kbrd(message: types.Message, bot: Bot, id: int):
    await asyncio.sleep(30)
    await message.delete()
    await bot.delete_message(chat_id=USER_CHAT, message_id=id)

#______________________________________________________________________________________________________________________________________
@user_group.message(Command("faq"))
async def FAQ_cmd(message: types.Message, session: AsyncSession, bot: Bot):
    id = await message.answer('Пожалуйста, выберите вопрос который Вас беспокоит', reply_markup = await choice_qq_btns(session))
    print(id.message_id)
    await del_inline_kbrd(message, bot, id.message_id)

#______________________________________________________________________________________________________________________________________
@user_group.callback_query(ChoiceQQ.filter())
async def work_pagination_handler(call: types.CallbackQuery, callback_data: ChoiceQQ, session: AsyncSession):
    """ Навигация по списку работ """
    page = callback_data.page
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=await choice_qq_btns(session, page=page))  # Обновление клавиатуры при нажатии кнопок навигации

#______________________________________________________________________________________________________________________________________
@user_group.callback_query(F.data.startswith('q_'))
async def get_work(callback: types.CallbackQuery, session: AsyncSession, bot: Bot):
    await bot.send_chat_action(chat_id=callback.from_user.id, action='typing')
    question = callback.data.split('_')[-1]
    solution = await orm_get_one_ques(session, question)
    await callback.answer(f'Вопрос {question}')
    
    await callback.message.answer(
        f'<b><i>Вопрос:</i></b>\n{solution.problem}\n\n<b>Решение:</b>\n{solution.answer}'
    )
#______________________________________________________________________________________________________________________________________