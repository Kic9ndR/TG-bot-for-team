from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import *


# Настраиваемые кнопки
def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


# CallBack и URL кнопки
def get_url_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


#Создать микс из CallBack и URL кнопок
def get_inlineMix_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


############################################################################################
class ChoiceQQ(CallbackData, prefix="Questions"):
    action: str                                 # Вперед и назад для кнопок навигации
    page: int = 0                               # Страница с работниками

# Выбор сотрудника
async def choice_qq_btns(
        session: AsyncSession,
        sizes = (1,2,),
        page: int = 0,
        ):

    keyboard = InlineKeyboardBuilder()
    start_offset = page * 8
    limit = 8
    end_offset = start_offset + limit
    qq = await orm_get_qq(session)

    keyboard.add(InlineKeyboardButton(text=f"Страница {page + 1}", callback_data='page'))  # Добавление кнопки "страница"
    for question in qq[start_offset:end_offset]:
        keyboard.add(InlineKeyboardButton(text=f'{question.contents}', callback_data=f"q_{question.contents}"))
        
    keyboard.adjust(*sizes)

    buttons_row = []                                        # Создание списка кнопок
    if page > 0:                                            # Проверка, что страница не первая
        buttons_row.append(InlineKeyboardButton(text="⬅️", callback_data=ChoiceQQ(action="prev", page=page - 1).pack()))  # Добавление кнопки "назад"
    if end_offset < len(qq):                                # Проверка, что ещё есть вопросы для следующей страницы
        buttons_row.append(InlineKeyboardButton(text="➡️", callback_data=ChoiceQQ(action="next", page=page + 1).pack()))  # Добавление кнопки "вперед"

    keyboard.adjust(*sizes)

    return keyboard.row(*buttons_row).as_markup()