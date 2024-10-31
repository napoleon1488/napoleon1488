import telebot
from telebot import types
import time
import threading

# Replace with your API key
API_TOKEN = '7801536760:AAGn39Z_Zo3FG_Felze0Jgn_GYVeaxBO_y0'

# Основной канал и дополнительный канал для обязательной подписки
CHANNEL_NAME = 'TradeAdoptMe | MurderMystary2'
CHANNEL_USERNAME = 'adoptrobloxx'
CHANNEL_LINK = f'https://t.me/{CHANNEL_USERNAME}'

SECOND_CHANNEL_NAME = 'PetsGoTG'
SECOND_CHANNEL_USERNAME = 'PetsGoTG'
SECOND_CHANNEL_LINK = f'https://t.me/{SECOND_CHANNEL_USERNAME}'

FREE_RBX_CHANNEL = 'https://t.me/freerbxtut'

bot = telebot.TeleBot(API_TOKEN)

ALLOWED_CHAT_IDS = [-1002168598620, -1002170011623]

# Function to check subscription and send notifications
def send_subscription_reminder(user_id, chat_id, mention):
    while True:
        if not check_subscriptions(user_id):
            markup = types.InlineKeyboardMarkup()

            # Кнопки для обязательной подписки на оба канала
            channel_button = types.InlineKeyboardButton(
                f'Подписаться на {CHANNEL_NAME} 🔑', url=CHANNEL_LINK)
            second_channel_button = types.InlineKeyboardButton(
                f'Подписаться на {SECOND_CHANNEL_NAME} 🐾', url=SECOND_CHANNEL_LINK)
            markup.add(channel_button, second_channel_button)

            bot.send_message(
                chat_id,
                f'{mention}, подпишитесь на сообщества ниже, чтобы получить возможность писать сообщения в чат\n\n'
                f'<a href="{FREE_RBX_CHANNEL}"><b>Бесплатные робуксы</b> 📦</a>',
                reply_markup=markup,
                parse_mode="HTML")
        time.sleep(10)

# Check if the chat is allowed
def is_allowed_chat(chat_id):
    return chat_id in ALLOWED_CHAT_IDS

# Handler for new chat members
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    chat_id = message.chat.id

    if not is_allowed_chat(chat_id):
        return

    user_id = message.new_chat_members[0].id
    username = message.new_chat_members[0].username
    first_name = message.new_chat_members[0].first_name

    mention = f"@{username}" if username else f"<a href='tg://user?id={user_id}'>{first_name or 'Пользователь'}</a>"

    markup = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton(f'Подписаться на {CHANNEL_NAME} 🔑', url=CHANNEL_LINK)
    second_channel_button = types.InlineKeyboardButton(f'Подписаться на {SECOND_CHANNEL_NAME} 🐾', url=SECOND_CHANNEL_LINK)
    markup.add(channel_button, second_channel_button)

    bot.send_message(
        chat_id,
        f'Привет, {mention}! Подпишитесь на сообщества ниже, чтобы получить возможность писать сообщения в чат\n\n'
        f'<a href="{FREE_RBX_CHANNEL}"><b>Бесплатные робуксы</b> 📦</a>',
        reply_markup=markup,
        parse_mode="HTML")

    thread = threading.Thread(target=send_subscription_reminder,
                              args=(user_id, chat_id, mention))
    thread.start()

# Function to check subscription status for both channels
def check_subscriptions(user_id):
    try:
        # Проверка подписки на первый канал
        first_channel_status = bot.get_chat_member(f'@{CHANNEL_USERNAME}', user_id).status
        # Проверка подписки на второй канал
        second_channel_status = bot.get_chat_member(f'@{SECOND_CHANNEL_USERNAME}', user_id).status
        if first_channel_status not in ['member', 'administrator', 'creator'] or \
           second_channel_status not in ['member', 'administrator', 'creator']:
            return False
    except Exception:
        return False
    return True

# Handler for all message types
@bot.message_handler(content_types=[
    'text', 'photo', 'video', 'animation', 'document', 'audio', 'voice', 'sticker'
])
def check_user_permissions(message):
    chat_id = message.chat.id

    if not is_allowed_chat(chat_id):
        return

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    mention = f"@{username}" if username else f"<a href='tg://user?id={user_id}'>{first_name or 'Пользователь'}</a>"

    if not check_subscriptions(user_id):
        try:
            bot.delete_message(chat_id, message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            if e.result['description'] == "Bad Request: message to delete not found":
                print(f"Ошибка: не удалось найти сообщение для удаления. ID сообщения: {message.message_id}")
            else:
                raise e  # Raise for other Telegram API errors

        markup = types.InlineKeyboardMarkup()
        channel_button = types.InlineKeyboardButton(f'Подписаться на {CHANNEL_NAME} 🔑', url=CHANNEL_LINK)
        second_channel_button = types.InlineKeyboardButton(f'Подписаться на {SECOND_CHANNEL_NAME} 🐾', url=SECOND_CHANNEL_LINK)
        markup.add(channel_button, second_channel_button)

        bot.send_message(
            chat_id,
            f'{mention}, подпишитесь на сообщества ниже, чтобы получить возможность писать сообщения в чат\n\n'
            f'<a href="{FREE_RBX_CHANNEL}"><b>Бесплатные робуксы</b> 📦</a>',
            reply_markup=markup,
            parse_mode="HTML")

# Start the bot with a 3-second interval between requests
bot.polling(none_stop=True, interval=3)
