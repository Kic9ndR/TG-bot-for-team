from aiogram.types import BotCommand

admin = [
    BotCommand(command='add_question', description='Добавление нового вопроса 😎')
]

client = [
    BotCommand(command='faq', description='Часто задаваемые вопросы'),
    BotCommand(command='another', description='Просто есть что-то'),
    BotCommand(command='fuq', description='Noy')
]