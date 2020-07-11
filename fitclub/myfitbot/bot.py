import telebot
from telebot import types
#from users import utils
from myfitbot import utils
from myfitbot.markup import Keyboards
from schedules.schedules import CustomPDF
import re

from mainfitclub import settings


token = settings.TOKEN
bot = telebot.TeleBot(token)

# @bot.message_handler(commands=["start"])
# def start_command(message):
#     keyboard = Keyboards().start_menu()
#     bot.send_message(
#         message.chat.id, 'Привет',
#         reply_markup=keyboard
#     )

# Обработчик текста при нажатии на кнопку

@bot.message_handler(content_types=["text"])
def set_text_callback(message):
    if message.text == 'Сформировать новую карту' or \
            message.text == 'Добавить услугу в карту клиента':
        keyboard = Keyboards().category_menu()
        bot.send_message(
            message.chat.id, 'Выберите категорию',
            reply_markup=keyboard
        )
    elif message.text == 'Показать текущую корзину':
        current_basket(message)
    elif message.text == 'log':
        log_handler(message)
    elif message.text == '/password':
        pass_handler(message)
    elif message.text == 'logout':
        logout_command(message)
    elif message.text == 'Создать карту клиента':
        card_create_command(message)
    elif message.text == 'Ваши карты клиента':
        get_all_cards(message)
    elif message.text == 'Оплатить карту':
        process_buy_command(message)


# @bot.message_handler(commands=["users"])
# def users_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(
#         telebot.types.InlineKeyboardButton('Users', callback_data='get-users')
#     )
#     bot.send_message(
#         message.chat.id,
#         'Click on the currency of choice:',
#         reply_markup=keyboard
#     )

# Обработка нажатий на inline кнопок

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    # if data.startswith('get-'):
    #     get_users_callback(query)

    if data.startswith('service'):
        get_dates_callback(query)

    elif data.startswith('date'):
        get_periods_callback(query)

    elif data.startswith('period'):
        get_for_basket(query)

    elif data.startswith('card'):
        get_card_callback(query)

    elif data.startswith('delete_msg'):
        global MSG_ID
        MSG_ID = data.split()[1]
        delete_msg_callback(query)

    elif data.startswith('pass_del'):
        global MSG_REG_ID
        MSG_REG_ID = data.split()[1]
        pass_del_callback(query)
    else:
        get_services_on_category(query)


# def get_users_callback(query):
#     bot.answer_callback_query(query.id)
#     send_users_result(query.message)
#
#
# def send_users_result(message):
#     bot.send_chat_action(message.chat.id, 'typing')
#     users = utils.get_users()
#     for user in users:
#         bot.send_message(
#             message.chat.id, serialize_user(user),
#             parse_mode='HTML'
#         )
#
#
# def serialize_user(user):
#     result = '<b>' + user['username'] + ' -> ' + user['email'] + '</b>\n\n'
#     return result


def get_services_on_category(query):
    bot.answer_callback_query(query.id)
    send_services_result(query.message, cat_id=query.data)
    print(query)


def send_services_result(message, cat_id):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = Keyboards().service_on_category_menu(cat_id)
    bot.send_message(
        message.chat.id,
        'Выберите услугу:',
        reply_markup=keyboard
    )


def get_dates_callback(query):
    data = query.data.split(':')
    global SERVICE_ID
    SERVICE_ID = data[1]
    service_name = data[2]
    bot.answer_callback_query(query.id, f'Вы выбрали {service_name}', show_alert=True)
    send_dates_result(query.message)
    print(query)


def send_dates_result(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = Keyboards().dates_menu()
    bot.send_message(
        message.chat.id,
        'Выберите желаемую дату:',
        reply_markup=keyboard
    )


def get_periods_callback(query):
    data = query.data.split(':')
    global DATE_ID
    DATE_ID = data[1]
    date_name = data[2]
    bot.answer_callback_query(query.id, f'Вы выбрали {date_name}', show_alert=True)
    send_periods_result(query.message)
    print(query)


def send_periods_result(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = Keyboards().period_menu()
    bot.send_message(
        message.chat.id,
        'Выберите желаемое время тренировки:',
        reply_markup=keyboard
    )


def get_for_basket(query):
    data = query.data.split()
    global PERIOD_ID
    PERIOD_ID = data[1]
    period_name = data[2]
    bot.answer_callback_query(query.id, f'Вы выбрали {period_name}', show_alert=True)
    put_in_basket(query.message)
    print(query)

def put_in_basket(message):
    utils.send_basket(DATE_ID, PERIOD_ID, SERVICE_ID, TOKEN_LOG)
    basket = utils.get_basket(TOKEN_LOG)
    print(basket)
    service = basket[-1]['service_id']
    date = basket[-1]['date']
    period = basket[-1]['time_period']
    price = basket[-1]['price']
    keyboard = Keyboards().basket_menu()
    bot.send_message(
        message.chat.id,
        f'Вы выбрали услугу: \n '
        f'{service} \n '
        f'Цена {price} руб. \n '
        f'Дата тренировки {date} \n '
        f'Время тренировки {period} \n',
        reply_markup=keyboard
    )










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


def current_basket(message):
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


def card_create_command(message):
    utils.create_card(TOKEN_LOG)
    global CARD_NUM
    numbers = utils.get_cards_nums(TOKEN_LOG)
    print(numbers)
    CARD_NUM = numbers[-1]['card_number']
    # bot.send_message(
    #     message.chat.id, 'Ok, Вы сформировали карту клиента')
    send_card_result(message)


def get_all_cards(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = Keyboards().cards_menu(TOKEN_LOG)
    bot.send_message(
        message.chat.id,
        'Выберите вашу карту',
        reply_markup=keyboard
    )


def get_card_callback(query):
    data = query.data.split()
    bot.answer_callback_query(query.id)
    CARD_NUM = data[1]
    send_card_result(query.message)


def send_card_result(message):
    global CARD_COST
    card = utils.get_card(CARD_NUM, TOKEN_LOG)
    user = card[0]['user']
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
    keyboard = Keyboards().make_payment()
    bot.send_message(message.chat.id, 'Для оплаты нажмите', reply_markup=keyboard
                     )


@bot.message_handler(commands=['reg'])
def reg_handler(message):
    msg = bot.send_message(message.chat.id, 'Введите ваш email')
    bot.register_next_step_handler(msg, ask_reg)


def ask_reg(message):
    global EMAIL_REG
    EMAIL_REG = message.text
    tpl = "[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
    if re.match(tpl, EMAIL_REG) is not None:
        bot.send_message(
            message.chat.id, 'Для ввода пароля нажмите /pass_reg')
    else:
        msg = bot.send_message(
            message.chat.id, 'Вы ввели неправильный email, попробуйте еще раз')
        bot.register_next_step_handler(msg, ask_reg)


@bot.message_handler(commands=['pass_reg'])
def pass_reg_handler(message):
    msg = bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(msg, ask_pas_reg)


def ask_pas_reg(message):
    global PASS_REG
    PASS_REG = message.text
    msg_id = message.message_id
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Подтвердить', callback_data=f'pass_del {msg_id}'))
    bot.send_message(
        message.chat.id, 'Ок, нажмите Подтвердить',
        reply_markup=keyboard)


def pass_del_callback(query):
    bot.answer_callback_query(query.id)
    delete_pass_msg(query.message)


def delete_pass_msg(message):
    bot.delete_message(message.chat.id, MSG_REG_ID)
    try:
        utils.make_reg(EMAIL_REG, PASS_REG)
        token = utils.get_token_login(EMAIL_REG, PASS_REG)['key']
        if token:
            bot.send_message(message.chat.id, 'Вы зарегистрированы, для входа нажмите /log')
    except KeyError:
        bot.send_message(message.chat.id, 'Пользователь с таким email уже зарегистрирован.'

                                          'Попробуйте еще разок /reg')


#@bot.message_handler(commands=['log'])
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


#@bot.message_handler(commands=['password'])
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
        keyboard = Keyboards().start_menu()
        bot.send_message(
            message.chat.id, 'Вы вошли в систему',
            reply_markup=keyboard
        )
        #bot.send_message(message.chat.id, 'Вы вошли в систему')
    except KeyError:
        bot.send_message(message.chat.id, 'Вы ввели неверный login или password.'
  
                                          'Попробуйте еще разок /log')


#@bot.message_handler(commands=["logout"])
def logout_command(message):
    utils.token_logout(TOKEN_LOG)
    bot.send_message(message.chat.id, 'Вы вышли из системы')


#@bot.message_handler(commands=['buy'])
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