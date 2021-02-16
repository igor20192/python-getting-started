###
###

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, AGS, CITY, WEATHER, PHOTO, DATA, STICKERS = range(7)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет я igor_bot.Как тебя зовут")
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    n = context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )

    update.message.reply_text(f"Приятно познакомиться {n['text']}.Сколько Вам лет")
    return AGS


def city(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("В каком городе живете")
    return CITY


def weather(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Какая у Вас погода")
    return WEATHER


def otwet(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text("Пришлите свое фото ")
    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("user_photo.png")
    update.message.reply_text("Спасибо! Высылаю свое ")
    update.message.reply_photo(
        "https://lh3.googleusercontent.com/7ohbL5_56aOqfXt5Nej8STAAY8wZRFQTbk72c5TFjsEdiHtEbafyyhEGvSicSI0QDdKZIA=s136"
    )
    reply_keyboard = [["Зима", "Весна", "Лето", "Осень"]]
    update.message.reply_text(
        "Назовите любимое время года",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return DATA


def vremgod(update: Update, context: CallbackContext) -> str:
    s = update.message.text
    update.message.reply_text(
        f" Ваше любимое время года{s} Пришлите stickers",
        reply_markup=ReplyKeyboardRemove(),
    )
    return STICKERS


def sticker(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Спасибо")
    update.message.reply_sticker(
        "https://s.tcdn.co/697/ba1/697ba160-9c77-3b1a-9d97-86a9ce75ff4d/93.png"
    )


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    updater = Updater("1611999120:AAEjmujFfVNAZoh4Y2Oq8WtPFnJSuJHnyvA")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            AGS: [MessageHandler(Filters.text, city)],
            CITY: [MessageHandler(Filters.text, weather)],
            WEATHER: [MessageHandler(Filters.text, otwet)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            DATA: [MessageHandler(Filters.regex("^(Зима|Весна|Осень|Лето)$"), vremgod)],
            STICKERS: [MessageHandler(Filters.sticker, sticker)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

