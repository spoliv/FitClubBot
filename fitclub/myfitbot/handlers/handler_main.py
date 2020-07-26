from myfitbot.handlers.handler_text import HandlerAllText
# импортируем класс HandlerInlineQuery обработка нажатия на кнопки инлайн
from myfitbot.handlers.handler_inline_query import HandlerInlineQuery
from myfitbot.handlers.handler_pay import HandlerPayment


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # инициализируем обработчики
        self.handler_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot, self.handler_text)
        self.handler_pay = HandlerPayment(self.bot, self.handler_text)

    def handle(self):
        """
        Запускает все обработчики бота
        """
        self.handler_text.handle()
        self.handler_inline_query.handle()
        self.handler_pay.handle()