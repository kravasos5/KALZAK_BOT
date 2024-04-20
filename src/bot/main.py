import logging
import sys
from enum import Enum
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler, MessageHandler,
)
from telegram.ext.filters import ALL

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Стадии диалога
class StagesEnum(Enum):
    """Перечисление стадий диалога"""
    START_CONVERSATION: int = 1
    CHOOSE_STICKER_TYPE: int = 2
    CHECK_SUBSCRIPTION: int = 3
    AFTER_SEND_PHOTO: int = 4


# Callback data
class CallbackEnum(Enum):
    """Перечисление кодов ответа"""
    DEFAULT_STICKERS: int = 1
    CUSTOM_STICKERS: int = 2
    START_CHECK_SUBSCRIPTION: int = 3
    CHECK_SUBSCRIPTION: int = 4
    SEND_PHOTO: int = 5
    START_GENERATE: int = 6
    END: int = 7


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Функция запуска диалога с ботом"""
    # Получаю юзера
    user = update.message.from_user
    # Добавляю лог
    logger.info("User %s started the conversation.", user.first_name)
    # Создаю клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("Сгенерировать стикер пак",
                                 callback_data=str(CallbackEnum.START_CHECK_SUBSCRIPTION.value)),
            InlineKeyboardButton("Завершить работу", callback_data=str(CallbackEnum.END.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляю клавиатуру
    await update.message.reply_text("Что будем делать ?", reply_markup=reply_markup)
    return StagesEnum.START_CONVERSATION.value


async def start_check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Проверка подписки на тг канал"""
    # Получаю юзера
    user = update.callback_query.from_user
    query = update.callback_query
    # Добавляю лог
    logger.info("User %s started the subscribe checking process.", user['first_name'])
    keyboard = [
        [
            InlineKeyboardButton("Подписаться", url="https://t.me/kalzak_chat"),#https://t.me/rasti_s_it
            InlineKeyboardButton("Я уже подписан", callback_data=str(CallbackEnum.CHECK_SUBSCRIPTION.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Чтобы начать генерацию стикер пака с Вами в главной роли,\
                 подпишитесь на Telegram-канал "Чат | Расти с IT"',
        reply_markup=reply_markup
    )
    return StagesEnum.CHECK_SUBSCRIPTION.value


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Проверить подписку на тг канал"""
    query = update.callback_query
    # проверка
    user_id = query.from_user.id
    channel_id = "-1002068006897"
    chat_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if chat_member.status != "left":
        logger.info("Вы подписаны")
    else: logger.info("Вы НЕ подписаны")

    logger.info("Проверка прошла успешно")
    keyboard = [
        [
            InlineKeyboardButton("Дефолтный стикер пак", callback_data=str(CallbackEnum.DEFAULT_STICKERS.value)),
            InlineKeyboardButton("Кастомный стикер пак", callback_data=str(CallbackEnum.CUSTOM_STICKERS.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите, что хотите сгенерировать", reply_markup=reply_markup)
    return StagesEnum.CHOOSE_STICKER_TYPE.value


async def default_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Генерация обычного стикер пака"""
    query = update.callback_query
    user = query.from_user
    logger.info("User %s chose default sticker pack.", user['first_name'])

    await query.edit_message_text(
        text="Чтобы получить ваш уникальный стикерпак, загрузите, пожалуйста, свою фотографию.\n"
             "Следуйте советам:\n"
             "— на фото должно быть хорошо видно ваше лицо;\n"
             "— на фото не должно быть других лиц, кроме вашего;\n"
             "— желательно без головного убора и очков;\n"
             "— если вы носите очки, то попробуйте использовать фото без них;\n"
             "— не отправляйте фото животных, бот распознаёт только лица людей."
    )
    return StagesEnum.AFTER_SEND_PHOTO.value


async def custom_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сгенерировать шаблонный стикер пак"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Чтобы получить ваш уникальный стикерпак, загрузите, пожалуйста, шаблоны фотографий для стикерпака.\n"
             "Следуйте советам:\n"
             "— на фото должно быть хорошо видно лицо;\n"
             "— на фото должно быть одно лицо;\n"
             "— желательно без головного убора и очков;\n"
             "— не отправляйте фото животных, бот распознаёт только лица людей."
    )
    return StagesEnum.AFTER_SEND_PHOTO.value


async def after_send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка фото"""
    logger.info('after_send_photo дошло')
    return ConversationHandler.END


async def end_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершить работу"""
    logger.info('end_work дошло')
    return ConversationHandler.END


def main() -> None:
    """Функция инициализации бота"""
    application = Application.builder().token(settings.TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            StagesEnum.START_CONVERSATION.value: [
                CallbackQueryHandler(start_check_subscription,
                                     pattern="^" + str(CallbackEnum.START_CHECK_SUBSCRIPTION.value) + "$"),
                CallbackQueryHandler(end_work,
                                     pattern="^" + str(CallbackEnum.END.value) + "$"),
            ],
            StagesEnum.CHECK_SUBSCRIPTION.value: [
                CallbackQueryHandler(check_subscription,
                                     pattern="^" + str(CallbackEnum.CHECK_SUBSCRIPTION.value) + "$"),
            ],
            StagesEnum.CHOOSE_STICKER_TYPE.value: [
                CallbackQueryHandler(default_stickers, pattern="^" + str(CallbackEnum.DEFAULT_STICKERS.value) + "$"),
                CallbackQueryHandler(custom_stickers, pattern="^" + str(CallbackEnum.CUSTOM_STICKERS.value) + "$"),
            ],
            StagesEnum.AFTER_SEND_PHOTO.value: [
                CallbackQueryHandler(after_send_photo, pattern="^" + str(CallbackEnum.SEND_PHOTO.value) + "$"),
                # CallbackQueryHandler(custom_stickers, pattern="^" + str(CallbackEnum.CUSTOM_STICKERS.value) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    # Добавляю обработчик диалога
    application.add_handler(conv_handler)
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
