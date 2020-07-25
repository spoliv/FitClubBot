# импортируем библиотеку абстрактный класс
import abc
# импортируем разметку клавиатуры и клавиш
from myfitbot.markup import Keyboards


class Handler(metaclass=abc.ABCMeta):
    """
    Абстрактный класс патерна Chain of responsibility
    """
    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # инициализируем разметку кнопок в меню и экрана
        self.keyboard = Keyboards()


    @abc.abstractmethod
    def handle(self):
        pass