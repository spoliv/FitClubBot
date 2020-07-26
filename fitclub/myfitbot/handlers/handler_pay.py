from myfitbot.handlers.handler import Handler
from myfitbot import utils
from telebot import types
from schedules.schedules import CustomPDF


class HandlerPayment(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопоки
    """
    def __init__(self, bot, handler_text):
        super().__init__(bot)
        self.handler_text = handler_text

    def handle(self):

        @self.bot.pre_checkout_query_handler(func=lambda query: True)
        def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
            self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

        @self.bot.message_handler(content_types=['successful_payment'])
        def process_successful_payment(message: types.Message):
            transaction_num = message.successful_payment.provider_payment_charge_id
            if transaction_num is not None:
                utils.make_active(self.handler_text.card_num, self.handler_text.token_log)
                pdf = CustomPDF(orientation='L', unit='mm', format='A4', token=self.handler_text.token_log)
                # Создаем особое значение {nb}
                pdf.alias_nb_pages()
                pdf.add_page()
                pdf.simple_table(self.handler_text.card_num, spacing=2)
                pdf.output('schedule_club.pdf')
                utils.send_email(self.handler_text.email)
