import telebot
from telebot import types
from users import utils
from services import utils
from schedules.schedules import CustomPDF
import re

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
    elif data.startswith('delete_msg'):
        global MSG_ID
        MSG_ID = data.split()[1]
        delete_msg_callback(query)
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


@bot.message_handler(commands=["zakaz"])
def zakaz_command(message):
    pre_order = {}
    service = utils.get_service(SERVICE_ID)
    date = utils.get_date(DATE_ID)
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
    utils.send_basket(DATE_ID, PERIOD_ID, SERVICE_ID, TOKEN_LOG)
    basket = utils.get_basket(TOKEN_LOG)
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
    basket = utils.get_basket(TOKEN_LOG)
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
    utils.create_card(TOKEN_LOG)
    bot.send_message(
        message.chat.id, 'Ok, Вы сформировали карту клиента')


@bot.message_handler(commands=["cards"])
def cards_command(message):
    numbers = utils.get_cards_nums(TOKEN_LOG)
    for num in numbers:
        card_number = num['card_number']
        bot.send_message(
            message.chat.id, card_number)


@bot.message_handler(commands=["card"])
def card_command(message):
    global CARD_COST, CARD_NUM
    card = utils.get_card(8688, TOKEN_LOG)
    user = card[0]['user']
    CARD_NUM = card[0]['card_number']
    CARD_COST = card[0]['client_card_cost']
    bot.send_message(
        message.chat.id,
        f'Ok, {user} Вы сформировали карту клиента стоимостью {CARD_COST} руб. \n'
        f'Перечень услуг :')
    for item in card[0]['card_items']:
        service = item['service_id']
        date = item['date']
        time_period = item['time_period']
        bot.send_message(
            message.chat.id,
            f'{service}  {date}  {time_period}')
    bot.send_message(message.chat.id, 'Для оплаты нажмите /buy')


@bot.message_handler(commands=['log'])
def log_handler(message):
    msg = bot.send_message(message.chat.id, 'Введите логин (email)')
    bot.register_next_step_handler(msg, ask_log)


def ask_log(message):
    global EMAIL
    EMAIL = message.text
    tpl = "[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
    if re.match(tpl, EMAIL) is not None:
        bot.send_message(
            message.chat.id, 'Для ввода пароля нажмите /password')
    else:
        msg = bot.send_message(
            message.chat.id, 'Вы ввели неправильный email, попробуйте еще раз')
        bot.register_next_step_handler(msg, ask_log)
    print(EMAIL)


@bot.message_handler(commands=['password'])
def pass_handler(message):
    msg = bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(msg, ask_pas)


def ask_pas(message):
    global PASSWORD
    PASSWORD = message.text
    msg_id = message.message_id
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Подтвердить', callback_data=f'delete_msg {msg_id}'))
    bot.send_message(
        message.chat.id, 'Ок, нажмите Подтвердить',
        reply_markup=keyboard)

    print(PASSWORD, msg_id)


def delete_msg_callback(query):
    bot.answer_callback_query(query.id)
    delete_msg(query.message)


def delete_msg(message):
    bot.delete_message(message.chat.id, MSG_ID)
    global TOKEN_LOG
    try:
        TOKEN_LOG = utils.get_token_login(EMAIL, PASSWORD)['key']
        bot.send_message(message.chat.id, 'Вы вошли в систему')
    except KeyError:
        bot.send_message(message.chat.id, 'Вы ввели неверный login или password.'
  
                                          'Попробуйте еще разок /log')


@bot.message_handler(commands=["logout"])
def logout_command(message):
    utils.token_logout(TOKEN_LOG)
    bot.send_message(message.chat.id, 'Вы вышли из системы')


@bot.message_handler(commands=['buy'])
def process_buy_command(message):
    if settings.BUY_TOKEN.split(':')[1] == 'TEST':
        bot.send_message(message.chat.id, 'Детали платежа')
        bot.send_invoice(
            message.chat.id,
            title=f'Карта клиента № {CARD_NUM}',
            description='Здесь надо указать реквизиты тестовой карты',
            provider_token=settings.BUY_TOKEN,
            currency='rub',
            #is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[types.LabeledPrice(label='Руб.', amount=int(CARD_COST) * 100)],
            start_parameter='payment_of_client_card',
            invoice_payload='some-invoice-payload-for-our-internal-use'
        )


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message: types.Message):
    print('successful_payment:')
    print(message)
    transaction_num = message.successful_payment.provider_payment_charge_id
    if transaction_num is not None:
        utils.make_active(CARD_NUM, TOKEN_LOG)
        pdf = CustomPDF(orientation='L', unit='mm', format='A4', token=TOKEN_LOG)
        # Создаем особое значение {nb}
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.simple_table(CARD_NUM, spacing=2)
        pdf.output('schedule_club.pdf')
        utils.send_email(EMAIL)

    print(transaction_num)







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