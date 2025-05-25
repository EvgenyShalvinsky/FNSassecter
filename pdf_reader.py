# Библиотека для записи .pdf в массив данных для чтения
import re
import PyPDF2
# Библиотеки для анализа и чтения данных из массива
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure

# -----НАСТРОЙКИ И ПЕРЕМЕННЫЕ-------------------------------------------
# Пути к файлу для обработки
pdf_path = '.\\Data\\test.pdf'
# Создание объекта .pdf файла
pdfFileObj = open(pdf_path, 'rb')
# Анализ и сортировка объектов .pdf файла
pdfRead = PyPDF2.PdfReader(pdfFileObj)
# Словарь для записи контента
content_pdf = {}
# Список с общим контентом
page_content = []


# -----ФУНКЦИИ-------------------------------------------
# Функция для получения текста из .pdf
def get_text(element):
    # Получаем текст из объекта в виде строки
    line_text = element.get_text()
    # Возвращаем текст из объекта
    return line_text


# Функция для чтения текста из файла .pdf
def read_text(pdf_path):
    # получаем layout
    for page_layout in extract_pages(pdf_path):
        # получаем element
        for element in page_layout:
            # отбираем текст из элементов LTTextContainer
            if isinstance(element, LTTextContainer):
                line_text = get_text(element)
                # Заполняем список page_content
                page_content.append(str(line_text).replace('#', ''))

def find_okved_codes(text):
    """
    Находит коды ОКВЭД в тексте.

    Args:
        text (str): Текст для поиска.

    Returns:
        list: Список найденных кодов ОКВЭД.
    """
    okved_pattern = r'\d{2}\.\d{2}'
    dates_pattern = r'\d{2}\.\d{2}\.\d{4}'
    # Находим все коды ОКВЭД
    okved_codes = re.findall(okved_pattern, text)

    # Находим все даты
    dates = re.findall(dates_pattern, text)

    # Фильтруем коды ОКВЭД, чтобы исключить даты
    okved_codes = [code for code in okved_codes if code not in [date[:5] for date in dates]]

    return okved_codes

# Основная функция
def scan_pdf():
    # Записываем текст из .pdf в список page_content
    read_text(pdf_path)
    # Заполняем словарь content_pdf из списка page_content

    # Закрываем объект файла pdf
    pdfFileObj.close()

    return page_content



