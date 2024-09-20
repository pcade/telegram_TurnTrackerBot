import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
import schedule
import time
from datetime import datetime, timedelta

import dataClass
import config

UserManager = dataClass.UserManager()
Calendar    = dataClass.Calendar()

#print(Calendar.get_week(2))

userGrisha  = UserManager.find_user_by_username("Гриша")
userPolya   = UserManager.find_user_by_username("Поля")
userYasha   = UserManager.find_user_by_username("Яша")
userLena    = UserManager.find_user_by_username("Леночка")

#print(userGrisha.chat_id)
#print(userPolya.chat_id)
#print(userYasha.chat_id)
#print(userLena.chat_id)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Функция для планирования напоминаний
def schedule_reminders(bot):
    schedule.every().monday.at("10:59").do(send_reminder, bot)


def create_keyboard(weeks, selected_weeks):
    """Создает клавиатуру с кнопками для выбора недели, исключая уже выбранные недели."""
    keyboard = []
    for i, week in enumerate(weeks):
        if week not in selected_weeks:
            keyboard.append([InlineKeyboardButton(week, callback_data=str(i + 1))])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    weeks = Calendar.get_all_weeks()
    context.bot_data['weeks'] = weeks
    if 'selected_weeks' not in context.bot_data:
        context.bot_data['selected_weeks'] = {}
    selected_weeks = context.bot_data['selected_weeks'].keys()
    reply_markup = create_keyboard(weeks, selected_weeks)
    context.user_data['reply_markup'] = reply_markup
    context.user_data['started_user_id'] = update.message.from_user.id
    await update.message.reply_text('Выберите неделю в месяце:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатия кнопки."""
    query = update.callback_query
    await query.answer()

    # Проверка, что нажавший кнопку пользователь тот же, кто вызвал /start
    if query.from_user.id != context.user_data.get('started_user_id'):
       return

    week_index = int(query.data) - 1
    weeks = context.bot_data.get('weeks', [])
    if 0 <= week_index < len(weeks):
        selected_week = weeks[week_index]
        user_id = query.from_user.id
        username = query.from_user.username
        if selected_week not in context.bot_data['selected_weeks']:
            context.bot_data['selected_weeks'][selected_week] = {'user_id': user_id, 'username': username}
            await query.edit_message_text(text=f"Вы выбрали {selected_week}. Мы уведомим вас перед её наступлением.")
        else:
            await query.edit_message_text(text=f"Неделя {selected_week} уже была выбрана ранее.")
    else:
        await query.edit_message_text(text="Ошибка: неверный выбор недели.")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /remind."""
    selected_weeks = context.bot_data.get('selected_weeks', {})
    all_weeks = context.bot_data.get('weeks', [])
    free_weeks = [week for week in all_weeks if week not in selected_weeks]

    message = "Выбранные недели:\n"
    for week, user_info in selected_weeks.items():
        message += f"{week} - {user_info['username']}\n"

    message += "\nСвободные недели:\n"
    message += "\n".join(free_weeks) if free_weeks else "Нет свободных недель."

    await update.message.reply_text(message)
    

print(Calendar.get_all_weeks())
