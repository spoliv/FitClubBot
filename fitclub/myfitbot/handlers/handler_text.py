import re
from mainfitclub import settings
from telebot import types
from myfitbot.handlers.handler import Handler
from myfitbot import utils


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопоки
    """
    def __init__(self, bot):
        super().__init__(bot)

    def handle(self):
        @self.bot.message_handler(content_types=["text"])
        def set_text_callback(message):
            if message.text == 'Сформировать новую карту' or \
                    message.text == 'Добавить услугу в карту клиента':
                print(message)
                self.bot.delete_message(message.chat.id, message.message_id - 1)
                self.bot.delete_message(message.chat.id, message.message_id)
                self.bot.send_message(
                    message.chat.id, 'Выберите категорию',
                    reply_markup=self.keyboard.category_menu()
                )
            elif message.text == 'Показать текущую корзину':
                self.get_current_basket(message)
            elif message.text == 'Зарегистрироваться':
                self.reg_handler(message)
            elif message.text == '/pass_reg':
                self.pass_reg_handler(message)
            elif message.text == 'Войти' or message.text == '/log':
                self.log_handler(message)
            elif message.text == '/password':
                self.pass_handler(message)
            elif message.text == 'Выход':
                self.logout_command(message)
            elif message.text == 'Создать карту клиента':
                self.create_card(message)
            elif message.text == 'Ваши карты клиента':
                self.get_all_cards(message)
            elif message.text.split()[0] == 'Оплатить':
                self.process_buy_command(message)
            elif message.text.split()[0] == 'Удалить':
                self.del_service(message)
            elif message.text == 'Подтвердить':
                self.delete_msg(message)
            elif message.text == 'Подтвердить регистрацию':
                self.delete_pass_msg(message)
            elif message.text == '/start':
                self.bot.send_message(
                    message.chat.id,
                    'Для продолжения выберите',
                    reply_markup=self.keyboard.log_reg_menu()
                )

    # Удаление услуги из корзины
    def del_service(self, message):
        basket = utils.get_basket_for_card(self.token_log)
        try:
            bsk_id = basket[-1]['id']
            utils.clear_basket(bsk_id, self.token_log)
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.delete_message(message.chat.id, message.message_id - 1)
            self.bot.send_message(
                message.chat.id,
                'Для продолжения выберите',
                reply_markup=self.keyboard.basket_menu()
            )
        except IndexError:
            self.bot.send_message(message.chat.id, 'Ваша корзина пуста',
                                  reply_markup=self.keyboard.basket_menu())

    def get_current_basket(self, message):
        basket = utils.get_basket(self.token_log)
        msg_str = ''
        for item in basket:
            service = item['service_id']
            date = item['date']
            period = item['time_period']
            price = item['price']
            msg_str += f'{service} \n ' \
                f'Цена {price} руб. \n ' \
                f'Дата тренировки {date} \n ' \
                f'Время тренировки {period} \n \n'
        print(msg_str)
        self.bot.delete_message(message.chat.id, message.message_id - 1)
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
            message.chat.id, 'В Вашей корзине следующие услуги: \n' + msg_str,
            reply_markup=self.keyboard.basket_menu())

    def create_card(self, message):
        utils.create_card(self.token_log)
        numbers = utils.get_cards_nums(self.token_log)
        print(numbers)
        self.card_num = numbers[-1]['card_number']
        self.bot.delete_message(message.chat.id, message.message_id - 1)
        self.show_created_card(message)

    def get_all_cards(self, message):
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.delete_message(message.chat.id, message.message_id - 1)
        self.bot.send_message(
            message.chat.id,
            'Выберите вашу карту. Если у Вас нет карт сформируйте новую',
            reply_markup=self.keyboard.cards_menu(self.token_log)
        )
        print(message)

    def show_created_card(self, message):
        card = utils.get_card(self.card_num, self.token_log)
        user = card[0]['user']
        self.card_cost = card[0]['client_card_cost']
        msg_str = ''
        for item in card[0]['card_items']:
            service = item['service_id']
            date = item['date']
            time_period = item['time_period']
            msg_str += f'{service}  {date}  {time_period} \n'
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.send_message(
                    message.chat.id,
                    f'Ok, {user} \n Вы сформировали карту клиента стоимостью {self.card_cost} руб. \n '
                    f'Перечень услуг : \n' + msg_str, reply_markup=self.keyboard.make_payment())

    # Регистрация нового пользователя
    # @bot.message_handler(commands=['reg'])
    def reg_handler(self, message):
        self.bot.delete_message(message.chat.id, message.message_id - 1)
        self.bot.delete_message(message.chat.id, message.message_id)
        msg = self.bot.send_message(message.chat.id, 'Введите ваш email')
        self.bot.register_next_step_handler(msg, self.ask_reg)

    def ask_reg(self, message):
        self.email_reg = message.text
        tpl = "[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
        if re.match(tpl, self.email_reg) is not None:
            self.bot.send_message(
                message.chat.id, 'Для ввода пароля нажмите /pass_reg')
        else:
            msg = self.bot.send_message(
                message.chat.id, 'Вы ввели неправильный email, попробуйте еще раз')
            self.bot.register_next_step_handler(msg, self.ask_reg)

    def pass_reg_handler(self, message):
        msg = self.bot.send_message(message.chat.id, 'Введите пароль')
        self.bot.register_next_step_handler(msg, self.ask_pas_reg)

    def ask_pas_reg(self, message):
        self.pass_reg = message.text
        self.bot.send_message(
            message.chat.id, 'Ок, нажмите Подтвердить регистрацию',
            reply_markup=self.keyboard.confirm_pass_reg())

    def delete_pass_msg(self, message):
        self.bot.delete_message(message.chat.id, message.message_id - 2)
        try:
            utils.make_reg(self.email_reg, self.pass_reg)
            token = utils.get_token_login(self.email_reg, self.pass_reg)['key']
            if token:
                self.bot.send_message(message.chat.id, 'Вы зарегистрированы, для входа нажмите /log')
        except KeyError:
            self.bot.send_message(message.chat.id, 'Пользователь с таким email уже зарегистрирован.'

                                              'Попробуйте еще разок /reg')

    # Вход пользователя в систему
    def log_handler(self, message):
        self.bot.delete_message(message.chat.id, message.message_id - 1)
        self.bot.delete_message(message.chat.id, message.message_id)
        msg = self.bot.send_message(message.chat.id, 'Введите логин (email)')
        self.bot.register_next_step_handler(msg, self.ask_log)

    def ask_log(self, message):
        self.email = message.text
        tpl = "[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"
        if re.match(tpl, self.email) is not None:
            self.bot.send_message(
                message.chat.id, 'Для ввода пароля нажмите /password')
        else:
            msg = self.bot.send_message(
                message.chat.id, 'Вы ввели неправильный email, попробуйте еще раз')
            self.bot.register_next_step_handler(msg, self.ask_log)

    def pass_handler(self, message):
        msg = self.bot.send_message(message.chat.id, 'Введите пароль')
        self.bot.register_next_step_handler(msg, self.ask_pas)

    def ask_pas(self, message):
        self.password = message.text
        self.bot.send_message(
            message.chat.id, 'Ок, нажмите Подтвердить',
            reply_markup=self.keyboard.confirm_pass())

    def delete_msg(self, message):
        self.bot.delete_message(message.chat.id, message.message_id - 2)
        try:
            self.token_log = utils.get_token_login(self.email, self.password)['key']
            print(self.token_log)
            print(type(self.token_log))
            self.bot.send_message(
                message.chat.id, 'Вы вошли в систему',
                reply_markup=self.keyboard.start_menu()
            )
        except KeyError:
            self.bot.send_message(message.chat.id, 'Вы ввели неверный login или password.'

                                              'Попробуйте еще разок /log')

    def logout_command(self, message):
        utils.token_logout(self.token_log)
        self.bot.send_message(message.chat.id, 'Вы вышли из системы',
                              reply_markup=self.keyboard.log_reg_menu()
                              )

    def process_buy_command(self, message):
        if settings.BUY_TOKEN.split(':')[1] == 'TEST':
            self.bot.send_message(message.chat.id, 'Детали платежа')
            self.bot.send_invoice(
                message.chat.id,
                title=f'Карта клиента № {self.card_num}',
                description='Здесь надо указать реквизиты тестовой карты',
                provider_token=settings.BUY_TOKEN,
                currency='rub',
                # is_flexible=False,  # True если конечная цена зависит от способа доставки
                prices=[types.LabeledPrice(label='Руб.', amount=int(self.card_cost) * 100)],
                start_parameter='payment_of_client_card',
                invoice_payload='some-invoice-payload-for-our-internal-use'
            )



