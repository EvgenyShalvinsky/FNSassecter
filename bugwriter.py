import pathlib
import datetime
import hashlib

def write_report(name, report_id, lvl, description, result, fact):
    report = pathlib.Path(".\\Bugs\\report.txt")
    report.write_text(
        f'\nBUG REPORT'
        f'\n\nHASH: {hashlib.sha256(b'datetime.datetime.now()').hexdigest()}'
        f'\nДата : {datetime.datetime.now()}'
        f'\nНАЗВАНИЕ :'
        f'\n{name}'
        f'\n\nID : {report_id}'
        f'\n\nУРОВЕНЬ : {lvl}'
        f'\n\nОПИСАНИЕ :'
        f'\n{description}'
        f'\n\nОЖИДЕМЫЙ РЕЗУЛЬТАТ :'
        f'\n{result}'
        f'\n\nФАКТИЧЕСКИЙ РЕЗУЛЬТАТ :'
        f'\n{fact}'


    )