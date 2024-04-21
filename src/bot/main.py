import logging
import sys
from enum import Enum
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Sticker, StickerSet
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler, MessageHandler, filters,
)

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
    BEFORE_SEND_PHOTO: int = 4
    BEFORE_SEND_PHOTOS: int = 5
    SEND_PHOTOS: int = 6
    AFTER_SEND_PHOTOS: int = 7


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
    STOP_PHOTOS: int = 8


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
    query = update.callback_query
    user = query.from_user
    # Добавляю лог
    logger.info("User %s started the subscribe checking process.", user['first_name'])
    keyboard = [
        [
            InlineKeyboardButton("Подписаться", url="https://t.me/kalzak_chat"),  # https://t.me/rasti_s_it
            InlineKeyboardButton("Я уже подписан", callback_data=str(CallbackEnum.CHECK_SUBSCRIPTION.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Чтобы начать генерацию стикер пака с Вами в главной роли, ' +
             'подпишитесь на Telegram-канал "Чат | Расти с IT"',
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
    else:
        logger.info("Вы НЕ подписаны")

    logger.info("Проверка прошла успешно")
    keyboard = [
        [
            InlineKeyboardButton("Обычный стикер пак", callback_data=str(CallbackEnum.DEFAULT_STICKERS.value)),
            InlineKeyboardButton("Пользовательский стикер пак", callback_data=str(CallbackEnum.CUSTOM_STICKERS.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите, что хотите сгенерировать", reply_markup=reply_markup)
    return StagesEnum.CHOOSE_STICKER_TYPE.value


async def default_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Генерация обычного стикер пака"""
    query = update.callback_query
    context.user_data['photos'] = []
    context.user_data['is_default'] = True

    keyboard = [
        [
            InlineKeyboardButton("Отмена", callback_data=str(CallbackEnum.END.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        reply_markup=reply_markup,
        text="Чтобы получить ваш уникальный стикерпак, загрузите, пожалуйста, свою фотографию.\n"
             "Следуйте советам:\n"
             "— на фото должно быть хорошо видно ваше лицо;\n"
             "— на фото не должно быть других лиц, кроме вашего;\n"
             "— желательно без головного убора и очков;\n"
             "— если вы носите очки, то попробуйте использовать фото без них;\n"
             "— не отправляйте фото животных, бот распознаёт только лица людей."
    )
    return StagesEnum.AFTER_SEND_PHOTOS.value


async def custom_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сгенерировать шаблонный стикер пак"""
    query = update.callback_query
    context.user_data['photos'] = []
    context.user_data['is_default'] = False
    keyboard = [
        [
            InlineKeyboardButton("Отмена", callback_data=str(CallbackEnum.END.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        reply_markup=reply_markup,
        text="Чтобы получить ваш уникальный стикерпак, загрузите, пожалуйста, шаблоны фотографий для стикерпака.\n"
             "Следуйте советам:\n"
             "— на фото должно быть хорошо видно лицо;\n"
             "— на фото должно быть одно лицо;\n"
             "— желательно без головного убора и очков;\n"
             "— не отправляйте фото животных, бот распознаёт только лица людей."
    )
    return StagesEnum.BEFORE_SEND_PHOTOS.value


async def before_send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка отправки шаблонных фото"""
    logger.info('after_send_photo дошло')
    photo = await update.message.photo[-1].get_file()
    context.user_data['photos'].append(photo)
    if len(context.user_data['photos']) == 50:
        return await stop_sending_photos(update, context)
    keyboard = [
        [
            InlineKeyboardButton("Завершить отправку", callback_data=str(CallbackEnum.STOP_PHOTOS.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{len(context.user_data['photos'])} / 50 фото загружено. Хотите отправить ещё ?",
        reply_markup=reply_markup
    )
    return StagesEnum.BEFORE_SEND_PHOTOS.value


async def stop_sending_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершить отправку фото"""
    logger.info('Отправка фото завершена')
    keyboard = [
        [
            InlineKeyboardButton("Отмена", callback_data=str(CallbackEnum.END.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        'Отправка шаблонных фото завершена! Теперь отправьте ваше фото!',
        reply_markup=reply_markup
    )
    return StagesEnum.AFTER_SEND_PHOTOS.value


async def send_user_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправка фото пользователя"""
    user_photo = await update.message.photo[-1].get_file()
    context.user_data['user_photo'] = user_photo
    print(context.user_data['user_photo'])
    print(context.user_data['photos'])
    print(context.user_data['is_default'])
    # вызов сервиса замены лиц и отправка стикер пака юзеру

    bot = context.bot
    chat_id = update.message.chat_id
    file = await bot.get_file(context.user_data['user_photo'].file_id)

    # Загружаем фотографию
    photo_file = await file.download_to_drive()
    # Создаем стикер из загруженной фотографии
    sticker = Sticker(
        file_id=user_photo.file_id,
        emoji='😊',  # Эмодзи для стикера (можно изменить на нужное)
        file_unique_id=user_photo.file_id,
        height=50,
        width=50,
        is_animated=False,
        is_video=False,
        type="REGULAR"
    )
    # Создаем стикерпак
    sticker_set = StickerSet(
        name='YourStickerPack',  # Имя стикерпака
        title='Your Sticker Pack',  # Заголовок стикерпака
        stickers=[sticker],  # Добавляем созданный стикер в стикерпак
        sticker_type="REGULAR"
    )
    # Отправляем стикерпак пользователю
    await bot.create_new_sticker_set(
        user_id=chat_id,  # ID чата (можно использовать и другие ID)
        name=sticker_set.name,
        title=sticker_set.title,
        stickers=[sticker]
    )
    # Отправляем стикер в чат
    await bot.send_sticker(
        chat_id=chat_id,
        sticker=sticker.file_id
    )

    return ConversationHandler.END


async def end_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершить работу"""
    query = update.callback_query
    context.user_data['photos'] = []
    keyboard = [
        [
            InlineKeyboardButton("Сгенерировать стикер пак",
                                 callback_data=str(CallbackEnum.START_CHECK_SUBSCRIPTION.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        reply_markup=reply_markup,
        text="Чтобы начать заново, нажмите на кнопку"
    )
    return StagesEnum.START_CONVERSATION.value


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print('ДОШЛО')
    keyboard = [
        [
            InlineKeyboardButton("Сгенерировать стикер пак",
                                 callback_data=str(CallbackEnum.START_CHECK_SUBSCRIPTION.value)),
            InlineKeyboardButton("Завершить работу", callback_data=str(CallbackEnum.END.value)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляю клавиатуру
    await update.message.reply_text(
        text=f"Здравствуйте, {user.first_name}!\n"
             "Этот бот предназначен для генерации стикер паков.\n"
             "Чтобы сгенерировать стикер пак, следуйте инструкциям Бота и нажимайте на кнопки.\n"
             "Если возникли проблемы, можете написать админу @kravasos5.",
        reply_markup=reply_markup
    )
    return StagesEnum.START_CONVERSATION.value


def main() -> None:
    """Функция инициализации бота"""
    application = Application.builder().token(settings.TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("help", help_)
        ],
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
            StagesEnum.BEFORE_SEND_PHOTOS.value: [
                MessageHandler(filters.PHOTO, before_send_photos),
                CallbackQueryHandler(stop_sending_photos, pattern="^" + str(CallbackEnum.STOP_PHOTOS.value) + "$"),
                CallbackQueryHandler(end_work, pattern="^" + str(CallbackEnum.END.value) + "$"),
            ],
            StagesEnum.AFTER_SEND_PHOTOS.value: [
                MessageHandler(filters.PHOTO, send_user_photo),
                CallbackQueryHandler(end_work, pattern="^" + str(CallbackEnum.END.value) + "$"),
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
