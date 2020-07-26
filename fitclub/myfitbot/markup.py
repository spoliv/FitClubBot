from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove)

from myfitbot import utils
from myfitbot import config

import datetime
import calendar


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

        return KeyboardButton(name)

    def set_inline_btn(self, name, data=''):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        return InlineKeyboardButton(name, callback_data=data)

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
        itm_btn_3 = self.set_btn('Выход')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3)
        return self.markup

    def category_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=2)
        categories = utils.get_servicecategories()
        button_list = []
        for category in categories:
            if category['name'] == 'Trainers and PowerLifting':
                category_name = category['name'] + config.KEYBOARD['POWER']
                button_list.append(self.set_inline_btn(category_name, data=category['id']))
            elif category['name'] == 'Group Workouts':
                category_name = category['name'] + config.KEYBOARD['GROUP']
                button_list.append(self.set_inline_btn(category_name, data=category['id']))
            else:
                category_name = category['name'] + config.KEYBOARD['RELAX']
                button_list.append(self.set_inline_btn(category_name, data=category['id']))
        self.markup.add(*button_list)
        self.markup.row()
        return self.markup

    def service_on_category_menu(self, cat_id):
        """
        Создает разметку кнопок услуг по выбранной категории и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=2)
        button_list = []
        services = utils.get_services(cat_id)
        for service in services:
            service_id = service['id']
            service_name = service['name']
            button_list.append(self.set_inline_btn(service['name'], data=f'service:{service_id}:{service_name}'))
        self.markup.add(*button_list)
        self.markup.row()
        return self.markup

    def period_menu(self):
        """
        Создает разметку кнопок для выбора времени тренировки и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=3)
        periods = utils.get_periods()
        button_list = []
        for period in periods:
            period_id = period['id']
            period_name = period['period']
            button_list.append(self.set_inline_btn(period['period'], data=f'period {period_id} {period_name}'))
        self.markup.add(*button_list)
        self.markup.row()
        return self.markup

    def cards_menu(self, token):
        """
        Создает разметку кнопок с номером карты для выбора карты для просмотра и возвращает разметку
        """
        numbers = utils.get_cards_nums(token)
        if len(numbers) == 0:
            self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
            itm_btn_1 = self.set_btn('Сформировать новую карту')
            # рассположение кнопок в меню
            self.markup.row(itm_btn_1)
            return self.markup
        else:
            self.markup = InlineKeyboardMarkup(row_width=3)
            button_list = []
            for num in numbers:
                card_number = num['card_number']
                if num['is_active']:
                    card_number_paid = str(card_number) + config.KEYBOARD['PAID']
                    button_list.append(self.set_inline_btn(card_number_paid, data=f'card {card_number}'))
                else:
                    button_list.append(self.set_inline_btn(card_number, data=f'card {card_number}'))
            self.markup.add(*button_list)
            self.markup.row()
            return self.markup

    def basket_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Добавить услугу в карту клиента')
        itm_btn_2 = self.set_btn('Удалить услугу ' + config.KEYBOARD['DEL'])
        itm_btn_3 = self.set_btn('Показать текущую корзину')
        itm_btn_4 = self.set_btn('Создать карту клиента')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        self.markup.row(itm_btn_4)
        return self.markup

    def make_payment(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Оплатить карту ' + config.KEYBOARD['PAYMENT'])
        itm_btn_2 = self.set_btn('Ваши карты клиента')
        itm_btn_3 = self.set_btn('Сформировать новую карту')
        itm_btn_4 = self.set_btn('Выход')

        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        self.markup.row(itm_btn_4)
        return self.markup

    def confirm_pass(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('Подтвердить')
        # рассположение кнопок в меню
        self.markup.add(itm_btn_1)
        return self.markup

    def confirm_pass_reg(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('Подтвердить регистрацию')
        # рассположение кнопок в меню
        self.markup.add(itm_btn_1)
        return self.markup

# Формирование клавиатуры-календаря текущего месяца

    def create_callback_data(self, action, year, month, day):
        """ Create the callback data associated to each button"""
        return ";".join([action, str(year), str(month), str(day)])

    def separate_callback_data(self, data):
        """ Separate the callback data"""
        return data.split(";")

    def create_calendar(self):
        """
        Create an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns the InlineKeyboardMarkup object with the calendar.
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        data_ignore = self.create_callback_data("IGNORE", year, month, 0)
        self.markup = InlineKeyboardMarkup(row_width=7)
        # First row - Month and Year
        row = []
        row.append(self.set_inline_btn(calendar.month_name[month] + " " + str(year), data=data_ignore))
        self.markup.add(*row)
        # Second row - Week Days
        row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            row.append(self.set_inline_btn(day, data=data_ignore))
        self.markup.add(*row)

        my_calendar = calendar.monthcalendar(year, month)
        for week in my_calendar:
            row = []
            for day in week:
                if (day == 0) or day < now.day:
                    row.append(self.set_inline_btn(" ", data=data_ignore))
                else:
                    row.append(
                        self.set_inline_btn(str(day), data=f'date:{year}:{month}: {day}'))
            self.markup.add(*row)
        #Last row - Buttons
        # row = []
        # row.append(self.set_inline_btn("<", data=self.create_callback_data("PREV-MONTH", year, month, day)))
        # row.append(self.set_inline_btn(" ", data=data_ignore))
        # row.append(self.set_inline_btn(">", data=self.create_callback_data("NEXT-MONTH", year, month, day)))
        #keyboard.append(row)
        #self.markup.add(*row)

        return self.markup

    def log_reg_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('Зарегистрироваться')
        itm_btn_2 = self.set_btn('Войти')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        return self.markup