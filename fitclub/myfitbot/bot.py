# импортируем модуль телеграмбот из библиотеки pyTelegramBotAPI
import telebot
# импортируем основные настройки проекта
from mainfitclub import settings

# импортируем все обработчки бота
from myfitbot.handlers.handler_main import HandlerMain


class TelBot:
    """
    Основной класс телеграмм бота(Сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """

    def __init__(self):
        """
        Инициализация бота(Сервера)
        """
        # Получение токена
        self.token = settings.TOKEN
        # Инициализация бота на основе зарегистрированного токена
        self.bot = telebot.TeleBot(self.token)
        # Инициализация оброботчика событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        """
        Метод запускает основные события сервера
        """
        # обработчик событий
        self.start()
        # служит для запуска бота (работа в режиме нон-стоп)
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()