from aiogram.types import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                            KeyboardButton)



del_kb = ReplyKeyboardRemove()

#----------------------------------------------------------------------------------
nav_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Назад - вернуться на шаг назад. Отмена - отменить действие"
)