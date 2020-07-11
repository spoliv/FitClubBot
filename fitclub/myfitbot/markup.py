from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove)

from myfitbot import utils

class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки клавиатуры бота
    """

    # инициализация разметки
    def __init__(self):
        self.markup = None

    def set_btn(self, name):
        """
        Создает и возвращает кнопку по входным параметрам
        """
        # if name == "AMOUNT_ORDERS":
        #     config.KEYBOARD["AMOUNT_ORDERS"] = step
        #
        # if name == "AMOUNT_PRODUCT":
        #     config.KEYBOARD["AMOUNT_PRODUCT"] = "{}".format(quantity)
        #
        # if name == "APPLY":
        #     # создает кнопку оформить с данными о стоимости товара округленного до 2 - го знака после запятой
        #     config.KEYBOARD["APPLY"] = "{}({}) руб".format('✅ Оформить', step)

        return KeyboardButton(name)

    def set_inline_btn(self, name, data=''):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        # if len(data) == 0:
        #     data = str(name.id)
        return InlineKeyboardButton(str(name), callback_data=data)

    def remove_menu(self):
        """
        Удаляет данны кнопки и возвращает ее
        """
        return ReplyKeyboardRemove()


    def start_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Ваши карты клиента')
        itm_btn_2 = self.set_btn('Сформировать новую карту')
        itm_btn_3 = self.set_btn('FitBotClub')
        itm_btn_4 = self.set_btn('Настройки')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        return self.markup

    def category_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        categories = utils.get_servicecategories()
        for category in categories:
            self.markup.row(
                self.set_inline_btn(category['name'], data=category['id'])
            )
        return self.markup

    def service_on_category_menu(self, cat_id):
        """
        Создает разметку кнопок услуг по выбранной категории и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        services = utils.get_services(cat_id)
        for service in services:
            service_id = service['id']
            service_name = service['name']
            self.markup.row(
                self.set_inline_btn(service['name'], data=f'service:{service_id}:{service_name}')
            )
        return self.markup

    def dates_menu(self):
        """
        Создает разметку кнопок для выбора даты и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        dates = utils.get_dates()
        for date in dates:
            date_id = date['id']
            date_name = date['date']
            self.markup.row(
                self.set_inline_btn(date['date'], data=f'date:{date_id}:{date_name}')
            )
        return self.markup

    def period_menu(self):
        """
        Создает разметку кнопок для выбора времени тренировки и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        periods = utils.get_periods()
        for period in periods:
            period_id = period['id']
            period_name = period['period']
            self.markup.row(
                self.set_inline_btn(period['period'], data=f'period {period_id} {period_name}')
            )
        return self.markup

    def cards_menu(self, token):
        """
        Создает разметку кнопок с номером карты для выбора карты для просмотра и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        numbers = utils.get_cards_nums(token)
        for num in numbers:
            card_number = num['card_number']

            self.markup.row(
                self.set_inline_btn(card_number, data=f'card {card_number}')
            )
        return self.markup

    def basket_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Добавить услугу в карту клиента')
        itm_btn_2 = self.set_btn('Показать текущую корзину')
        itm_btn_3 = self.set_btn('Создать карту клиента')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        return self.markup

    def make_payment(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Оплатить карту')
        itm_btn_2 = self.set_btn('Ваши карты клиента')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        return self.markup