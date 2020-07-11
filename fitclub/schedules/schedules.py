import fpdf
from fpdf import FPDF
from myfitbot import utils


class CustomPDF(FPDF):

    def __init__(self, orientation, unit, format, token):
        self.token = token
        super(CustomPDF, self).__init__(orientation, unit, format)

    def header(self):
        # Устанавливаем лого
        self.image('E:/Курсовой проект 2020/FitClubBot/fitclub/images/club_logo.jpg', 10, 6, 30)
        self.add_font('DejaVu', '', 'C:\Windows\Fonts\DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)

        # Добавляем адрес
        self.cell(50)
        self.cell(0, 5, 'BodyFitClub', ln=1)
        self.ln(3)
        self.cell(50)
        self.cell(0, 5, 'г. Москва', ln=1)
        self.cell(50)
        self.cell(0, 5, 'ул. Бодибилдерная, 6', ln=1)
        self.ln(3)
        self.cell(50)
        self.cell(0, 5, 'Открыто: 9:00 - 21:00', ln=1)

        self.line(8, 40, 290, 40)
        self.set_line_width(1)

        # Line break Разрыв линии
        self.ln(20)

    def simple_table(self, crd_n, spacing=1):
        data = [['N n/n', 'Услуга', 'Дата', 'Время тренировки']]

        card = utils.get_card(crd_n, token=self.token)
        card_num = card[0]['card_number']
        name = card[0]['user']
        date_created = card[0]['date_created'][:10]
        print(date_created)
        self.cell(10, 5, f'Карта клиента {name}: {card_num} от {date_created}', ln=5)
        self.ln(10)
        self.cell(100)
        self.cell(50, 5, 'Расписание тренировок', ln=5)
        self.ln(10)

        num = 0
        for item in card[0]['card_items']:
            items = []
            num = num + 1
            items.append(str(num))
            service = item['service_id']
            items.append(service)
            date = item['date']
            items.append(date)
            time_period = item['time_period']
            items.append(time_period)
            data.append(items)


            #items.append(service, date, time_period)
        self.add_font('DejaVu', '', 'C:\Windows\Fonts\DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 12)
        col_width = self.w / 4.5
        row_height = self.font_size
        for row in data:
            for item in row:
                self.cell(col_width, row_height * spacing,
                         txt=item, border=1)
            self.ln(row_height * spacing)

    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)
        # Добавляем номер страницы
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')


# def create_pdf(pdf_path, crd_n):
#     pdf = CustomPDF(orientation='L', unit='mm', format='A4')
#     # Создаем особое значение {nb}
#     pdf.alias_nb_pages()
#     pdf.add_page()
#     pdf.simple_table(crd_n, spacing=2)
#     pdf.output(pdf_path)


#if __name__ == '__main__':
#     create_pdf('schedule_club.pdf', 6591)
