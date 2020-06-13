import telebot
from users import utils
#from ordersapp import utils
from services import utils

from mainfitclub import settings


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
    elif data.startswith('date'):
        global SERVICE_ID
        SERVICE_ID = data.split()[1]
        print(SERVICE_ID)

        #print(service_id[1])
        get_dates_callback(query)
    elif data.startswith('period'):
        global DATE_ID
        DATE_ID = data.split()[1]
        print(DATE_ID)
        get_periods_callback(query)
    elif data.startswith('train'):
        global PERIOD_ID
        PERIOD_ID = data.split()[1]
        print(PERIOD_ID)
        get_for_zakaz()
    else:
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
        service_id = service['id']
        keyboard.row(
            #telebot.types.InlineKeyboardButton(service['name'], callback_data=service['id'])
            telebot.types.InlineKeyboardButton(service['name'], callback_data=f'date {service_id}')
        )
    bot.send_message(
        message.chat.id,
        'Выберите услугу:',
        reply_markup=keyboard
    )


def get_dates_callback(query):
    bot.answer_callback_query(query.id)
    send_dates_result(query.message)
    print(query)


def send_dates_result(message):
    bot.send_chat_action(message.chat.id, 'typing')
    dates = utils.get_dates()
    keyboard = telebot.types.InlineKeyboardMarkup()
    #menu = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    # for date in dates:
    #     keyboard.row(
    #         telebot.types.InlineKeyboardButton(date['date'], callback_data='period')
    #     )
    for date in dates:
        date_id = date['id']
        row = telebot.types.InlineKeyboardButton(date['date'], callback_data=f'period {date_id}')
        keyboard.add(row)

    bot.send_message(
        message.chat.id,
        'Выберите желаемую дату:',
        reply_markup=keyboard
        #reply_markup = menu
    )


def get_periods_callback(query):
    bot.answer_callback_query(query.id)
    send_periods_result(query.message)
    print(query)


def send_periods_result(message):
    bot.send_chat_action(message.chat.id, 'typing')
    periods = utils.get_periods()
    keyboard = telebot.types.InlineKeyboardMarkup()
    for period in periods:
        period_id = period['id']
        keyboard.row(
            telebot.types.InlineKeyboardButton(period['period'], callback_data=f'train {period_id}')
        )
    bot.send_message(
        message.chat.id,
        'Выберите желаемое время тренировки:',
        reply_markup=keyboard
    )


def get_for_zakaz():
    print(f'SERVICE_ID = {SERVICE_ID}, DATE_ID = {DATE_ID}, PERIOD_ID = {PERIOD_ID}')


# service_id = SERVICE_ID
# date_id = DATE_ID
# period_id = PERIOD_ID


@bot.message_handler(commands=["zakaz"])
def zakaz_command(message):
    pre_order = {}
    service = utils.get_service(SERVICE_ID)
    #print(service)
    date = utils.get_date(DATE_ID)
    #print(date)
    period = utils.get_period(PERIOD_ID)
    quantity = service[0]['quantity']
    pre_order['name_service'] = service[0]['name']
    pre_order['date'] = date[0]['date']
    pre_order['period'] = period[0]['period']
    pre_order['price'] = service[0]['price']
    utils.send_order(DATE_ID, PERIOD_ID, SERVICE_ID, quantity)
    print(pre_order)
    bot.send_message(
        message.chat.id,
        'Вы выбрали услугу:' + '\n' +
        pre_order['name_service'] + '\n' +
        'Цена      ' + pre_order['price'] + 'руб.' + '\n' +
        'Дата тренировки     ' + pre_order['date'] + '\n' +
        'Время тренировки      ' + pre_order['period'] + '\n',

        #serialize_pre_order(pre_order),
        #parse_mode='HTML'
    )


@bot.message_handler(commands=["last"])
def basket_last_command(message):
    utils.send_basket(DATE_ID, PERIOD_ID, SERVICE_ID, 1)
    basket = utils.get_basket(1)
    print(basket)
    service = basket[-1]['service_id']
    date = basket[-1]['date']
    period = basket[-1]['time_period']
    price = basket[-1]['price']

    bot.send_message(
        message.chat.id,
        f'Вы выбрали услугу: \n '
        f'{service} \n '
        f'Цена {price} руб. \n '
        f'Дата тренировки {date} \n '
        f'Время тренировки {period} \n',

    )


@bot.message_handler(commands=["basket"])
def basket_command(message):
    basket = utils.get_basket(1)
    bot.send_message(
        message.chat.id,
        f'В Вашей корзине следующие услуги: \n ')
    for item in basket:
        service = item['service_id']
        date = item['date']
        period = item['time_period']
        price = item['price']
        bot.send_message(
            message.chat.id,
            f'{service} \n '
            f'Цена {price} руб. \n '
            f'Дата тренировки {date} \n '
            f'Время тренировки {period} \n',

        )


@bot.message_handler(commands=["create_card"])
def card_create_command(message):
    utils.create_card(1)
    #utils.create_card(1, 336)
    bot.send_message(
        message.chat.id, 'Ok, Вы сформировали карту клиента')


@bot.message_handler(commands=["card"])
def card_command(message):
    card = utils.get_card(1, 336)
    user = card[0]['user']
    card_cost = card[0]['client_card_cost']
    bot.send_message(
        message.chat.id,
        f'Ok, {user} Вы сформировали карту клиента стоимостью {card_cost} руб. \n'
        f'Перечень услуг :')
    for item in card[0]['card_items']:
        service = item['service_id']
        date = item['date']
        time_period = item['time_period']
        bot.send_message(
            message.chat.id,
            f'{service}  {date}  {time_period}')



# def serialize_pre_order(pre_order):
#     result = '<b>' + pre_order['name_service'] + '</b>\n\n' + \
#              '<b>' + 'Цена' + pre_order['price'] + 'руб.' + '</b>\n\n' + \
#              '<b>' + 'Дата тренировки' + pre_order['date'] + '</b>\n\n' + \
#              '<b>' + 'Время тренировки' + pre_order['period'] + '</b>\n\n'
#
#     return result


bot.polling(none_stop=True)

# if __name__ == '__main__':
#      bot.infinity_polling()