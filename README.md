# TG-bot-for-team

Телеграм-бот для управления вопросами и ответами с административной панелью.

## Описание

Этот бот позволяет администраторам добавлять вопросы и ответы в базу данных, которые затем могут быть доступны пользователям. Бот включает в себя функционал для:
- Добавления новых вопросов с оглавлением
- Управления ответами
- Административной панели для модерации

## Требования

- Python 3.8+
- aiogram
- SQLAlchemy
- Другие зависимости указаны в `requirements.txt`

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/TG-bot-for-team.git
cd TG-bot-for-team
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории и добавьте необходимые переменные окружения:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
```

## Использование

### Запуск бота

```bash
python main.py
```

### Административные команды

- `/add_question` - Добавить новый вопрос
- `/отмена` - Отменить текущее действие
- `/назад` - Вернуться к предыдущему шагу

## Структура проекта

```
TG-bot-for-team/
├── handlers/
│   ├── admin.py
│   └── user.py
├── database/
│   └── orm_query.py
├── filter/
│   └── chat_filters.py
├── kbrd/
│   └── reply.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Безопасность

- Не публикуйте токен бота и другие конфиденциальные данные
- Храните `.env` файл локально и не коммитьте его в репозиторий
- Регулярно обновляйте зависимости для исправления уязвимостей
