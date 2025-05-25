import time
from playwright.sync_api import sync_playwright
import download_pdf
import pathlib
import bugwriter
import logging
import zachetni

logging.basicConfig(level=logging.DEBUG)
#504207694645

def compare_lists(list1, list2):
    list1_sorted = sorted(list1)
    list2_sorted = sorted(list2)
    if len(list1_sorted) != len(list2_sorted):
        if len(list1_sorted) < len(list2_sorted):
            missing_elements = set(list2_sorted) - set(list1_sorted)
            return f"{missing_elements}"
        else:
            missing_elements = set(list1_sorted) - set(list2_sorted)
            return f"{missing_elements}"
    for i in range(len(list1_sorted)):
        if list1_sorted[i] != list2_sorted[i]:
            if list1_sorted[i] < list2_sorted[i]:
                return f"{list2_sorted[i]}"
            else:
                return f"{list1_sorted[i]}"

    return logging.info('коды ОКВЭД совпадают, скорее всего пользователь, требуется уточнение пользователя')

if __name__ == '__main__':
    logging.info(f'Начало работы ')
    inn_text = f'{input('Введите номер ИНН\n')}'
    #code_okved = f'{input('Введите ОКВЭД в формате 11.11\n')}'
    with sync_playwright() as playwright:
        zaokved = zachetni.get_okved_by_inn(playwright, inn_text)
    with sync_playwright() as playwright:
        download_pdf.run(playwright, inn_text)
    time.sleep(3)
    import pdf_reader
    text = ', '.join(pdf_reader.scan_pdf())
    okved_codes = pdf_reader.find_okved_codes(text)
    fns_list = set(sorted(okved_codes))
    za_list = set(sorted(zaokved))
    compare = compare_lists(fns_list, za_list)
    if compare == logging.info('ОКВЭД присутствует в выписке, скорее всего пользователь ошибся требуется уточнение'):
        pass
    else:
        bugwriter.write_report(
        name=f'Не совпадение ОКВЭД кодов на сайте ФНС egrul.nalog.ru  и https://zachestnyibiznes.ru/ ИНН : {inn_text}',
        report_id=f'OKWDERR{inn_text}',
        lvl=f'LOW',
        description=f'При сравнение номеров ОКВЭД на сайте ФНС egrul.nalog.ru  и https://zachestnyibiznes.ru/'
                    f'\nкомпании ИНН : {inn_text}, был найдены \nрасхождения в кодах ОКВЭД: \n {compare} ',
        result=f'Список ОКВЭД кодов на egrul.nalog.ru : {'\n'.join(fns_list)}',
        fact=f'Список ОКВЭД кодов на https://zachestnyibiznes.ru : {'\n'.join(za_list)}'
        )
    pathlib.Path.unlink(".\\Data\\test.pdf")
    print('очистка мусора')


