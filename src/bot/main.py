import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler, MessageHandler,
)
from telegram.ext.filters import ALL

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES, MAIN_MENU = range(3)
# Callback data
DEFAULT_STICKERS, CUSTOM_STICKERS, AFTER_SEND_PHOTO, CHECKED_SUBSCRIBE = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Дефолтный стикерпак", callback_data=str(DEFAULT_STICKERS)),
            InlineKeyboardButton("Кастомный стикерпак", callback_data=str(CUSTOM_STICKERS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Выберите, что хотите сгенерировать", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Дефолтный стикерпак", callback_data=str(DEFAULT_STICKERS)),
            InlineKeyboardButton("Кастомный стикерпак", callback_data=str(CUSTOM_STICKERS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Выберите, что хотите сгенерировать", reply_markup=reply_markup)
    return START_ROUTES


async def default_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Чтобы получить ваш уникальный стикерпак, загрузите, пожалуйста, свою фотографию.\n"
             "Следуйте советам:\n"
             "— на фото должно быть хорошо видно ваше лицо;\n"
             "— на фото не должно быть других лиц, кроме вашего;\n"
             "— желательно без головного убора и очков;\n"
             "— если вы носите очки, то попробуйте использовать фото без них;\n"
             "— не отправляйте фото животных, бот распознаёт только лица людей."
    )
    return AFTER_SEND_PHOTO


async def custom_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

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
    return AFTER_SEND_PHOTO


async def after_send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Подписаться", url="https://t.me/rasti_s_it"),
            InlineKeyboardButton("Я уже подписан", callback_data=str(CHECKED_SUBSCRIBE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text='Чтобы начать генерацию стикерпака с Вами в главной роли, подпишитесь на Telegram-канал "Чат | Расти с IT"',
        reply_markup=reply_markup
    )

    return CHECKED_SUBSCRIBE

async def checked_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Происходит магия превращения, скоро все получится...\n\n"
        "Как только все будет готов, мы пришлем уведомление",
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6767775067:AAGH2PAbT5m7r7tcDebbxdWLssk1qRCvRPs").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(default_stickers, pattern="^" + str(DEFAULT_STICKERS) + "$"),
                CallbackQueryHandler(custom_stickers, pattern="^" + str(CUSTOM_STICKERS) + "$"),
            ],
            CHECKED_SUBSCRIBE: [
                CallbackQueryHandler(checked_subscribe, pattern="^" + str(CHECKED_SUBSCRIBE) + "$"),
            ],
            AFTER_SEND_PHOTO: [
                MessageHandler(callback=after_send_photo, filters=ALL),
            ]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()