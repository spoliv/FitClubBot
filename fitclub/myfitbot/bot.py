import telebot
from fitclub.users import utils
from fitclub.services import utils
from fitclub.fitclub import settings


token = settings.TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["users"])
def users_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Users', callback_data='get-users')
    )
    bot.send_message(
        message.chat.id,
        'Click on the currency of choice:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_users_callback(query)
    get_services_callback(query)


def get_users_callback(query):
    bot.answer_callback_query(query.id)
    send_users_result(query.message)


def send_users_result(message):
    bot.send_chat_action(message.chat.id, 'typing')
    users = utils.get_users()
    for user in users:
        bot.send_message(
            message.chat.id, serialize_user(user),
            parse_mode='HTML'
        )


def serialize_user(user):
    result = '<b>' + user['username'] + ' -> ' + user['email'] + '</b>\n\n'
    return result


@bot.message_handler(commands=["categories"])
def category_command(message):
    categories = utils.get_servicecategories()
    keyboard = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        keyboard.row(
            telebot.types.InlineKeyboardButton(category['name'], callback_data=category['id'])
        )
        print(category['id'])
    bot.send_message(
        message.chat.id,
        'Выберите категорию услуг:',
        reply_markup=keyboard
    )


def get_services_callback(query):
    bot.answer_callback_query(query.id)
    send_services_result(query.message, cat_id=query.data)
    print(query)


def send_services_result(message, cat_id):
    bot.send_chat_action(message.chat.id, 'typing')
    services = utils.get_services(cat_id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    for service in services:
        keyboard.row(
            telebot.types.InlineKeyboardButton(service['name'], callback_data=service['id'])
        )
    bot.send_message(
        message.chat.id,
        'Выберите услугу:',
        reply_markup=keyboard
    )


bot.polling(none_stop=True)

# if __name__ == '__main__':
#      bot.infinity_polling()