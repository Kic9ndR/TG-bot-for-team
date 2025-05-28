import os
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, or_f, StateFilter
from filter.chat_filters import ChatFilter, IsAdmin
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.orm_query import *
from common.chat_cmds import admin
from kbrd.reply import * 

admin_router = Router()
admin_router.message.filter(ChatFilter(["private"]), IsAdmin())


#############################################################################################################
class UserQQ(StatesGroup):
    contents = State()
    question = State()
    answer = State()

    texts = {
    "UserQQ:contents": 'Напишите оглавление вопроса. <b>Ограничение 20 символов.</b>\nЭто краткое описание вопроса для пользователя.',
    "UserQQ:question": 'Напишите вопрос',
    "UserQQ:answer": 'Напиши ответ на вопрос',
    }

#############################################################################################################
@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=del_kb)

#__________________________________________________________________________________________________________
@admin_router.message(StateFilter(UserQQ), Command("назад"))
@admin_router.message(StateFilter(UserQQ), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == UserQQ.contents:
        await message.answer('Предыдущего шага нет, нажмите "Отмена"')
        return

    previous = None
    for step in UserQQ.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вернул к прошлому шагу\n{UserQQ.texts[previous.state]}")
            return
        previous = step

#############################################################################################################

@admin_router.message(StateFilter('*'), Command('add_question'))
async def question_cmd(message: types.Message, state: FSMContext):
    await message.answer("Напишите оглавление вопроса. <b>Ограничение 20 символов.</b>\nЭто краткое описание вопроса для пользователя.", reply_markup=nav_kb)
    await state.set_state(UserQQ.contents)
#_________________________________________________________________________________________   
@admin_router.message(UserQQ.contents)
async def add_question(message: types.Message, state: FSMContext):
    await state.update_data(contents=message.text)
    await message.answer("Напишите вопрос")
    await state.set_state(UserQQ.question)
#_________________________________________________________________________________________   
@admin_router.message(UserQQ.question)
async def add_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer("Напиши ответ на вопрос")
    await state.set_state(UserQQ.answer)
#_________________________________________________________________________________________
@admin_router.message(UserQQ.answer)
async def add_answer(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        await orm_add_question(
            session,
            contents=data['contents'],
            problem=data['question'],
            answer=data['answer'],
        )
        await message.answer('Добавил вопрос', reply_markup=del_kb)

    except Exception as e:
        await message.answer(f'Упс... Что-то пошло не так\n\n{e}', reply_markup=del_kb)
    