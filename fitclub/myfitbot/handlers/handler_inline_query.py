from myfitbot.handlers.handler import Handler

from myfitbot import utils


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на inline кнопоки
    """

    def __init__(self, bot, handler_text):
        super().__init__(bot)
        self.handler_text = handler_text

    def handle(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def iq_callback(query):
            data = query.data
            if data.startswith('service'):
                self.get_dates_callback(query)

            elif data.startswith('date'):
                self.get_periods_callback(query)

            elif data.startswith('period'):
                self.get_for_basket(query)

            elif data.startswith('card'):
                self.get_card_callback(query)
            else:
                self.get_services_on_category(query)

    def get_services_on_category(self, query):
        self.bot.answer_callback_query(query.id)
        self.send_services_result(query.message, cat_id=query.data)

    def send_services_result(self, message, cat_id):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
            message.chat.id,
            'Выберите услугу:',
            reply_markup=self.keyboard.service_on_category_menu(cat_id)
        )

    def get_dates_callback(self, query):
        data = query.data.split(':')
        self.service_id = data[1]
        service_name = data[2]
        self.bot.answer_callback_query(query.id, f'Вы выбрали {service_name}', show_alert=True)
        self.send_dates_result(query.message)

    def send_dates_result(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
            message.chat.id,
            'Выберите желаемую дату:',
            reply_markup=self.keyboard.create_calendar()
        )

    def get_periods_callback(self, query):
        data = query.data.split(':')
        day = data[3]
        month = data[2]
        year = data[1]
        date_name = f'{day}.{month}.{year}'
        utils.create_date(date_name)
        self.date_id = utils.get_dates()[-1]['id']
        self.bot.answer_callback_query(query.id, f'Вы выбрали {date_name}', show_alert=True)
        self.send_periods_result(query.message)

    def send_periods_result(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
            message.chat.id,
            'Выберите желаемое время тренировки:',
            reply_markup=self.keyboard.period_menu()
        )

    def get_for_basket(self, query):
        data = query.data.split()
        self.period_id = data[1]
        period_name = data[2]
        self.bot.answer_callback_query(query.id, f'Вы выбрали {period_name}', show_alert=True)
        self.put_in_basket(query.message)

    def put_in_basket(self, message):
        utils.send_basket(self.date_id, self.period_id, self.service_id, self.handler_text.token_log)
        basket = utils.get_basket(self.handler_text.token_log)
        service = basket[-1]['service_id']
        date = basket[-1]['date']
        period = basket[-1]['time_period']
        price = basket[-1]['price']
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
            message.chat.id,
            f'Вы выбрали услугу: \n '
            f'{service} \n '
            f'Цена {price} руб. \n '
            f'Дата тренировки {date} \n '
            f'Время тренировки {period} \n',
            reply_markup=self.keyboard.basket_menu()
        )

    def get_card_callback(self, query):
        data = query.data.split()
        self.bot.answer_callback_query(query.id)
        self.handler_text.card_num = data[1]
        self.send_card_result(query.message)

    def send_card_result(self, message):
        card = utils.get_card(self.handler_text.card_num, self.handler_text.token_log)
        user = card[0]['user']
        self.handler_text.card_cost = card[0]['client_card_cost']
        is_activated = card[0]['is_active']
        msg_str = ''
        for item in card[0]['card_items']:
            service = item['service_id']
            date = item['date']
            time_period = item['time_period']
            msg_str += f'{service}  {date}  {time_period} \n'
        self.bot.delete_message(message.chat.id, message.message_id)
        if is_activated:
            self.bot.send_message(
                message.chat.id,
                f'Вы уже оплатили эту карту клиента стоимостью {self.handler_text.card_cost} руб. \n'
                f'Перечень услуг : \n' + msg_str, reply_markup=self.keyboard.start_menu())
        else:
            self.bot.send_message(
                message.chat.id,
                f'Ok, {user} \n Вы сформировали карту клиента стоимостью {self.handler_text.card_cost} руб. \n '
                f'Перечень услуг : \n' + msg_str, reply_markup=self.keyboard.make_payment())