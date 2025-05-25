import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect


def get_okved_by_inn(playwright: Playwright, inn_text) -> None:
    global numeric_elements
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://zachestnyibiznes.ru/")
    page.get_by_role("searchbox", name="Submit").click()
    page.get_by_role("searchbox", name="Submit").fill(f'{inn_text}')
    page.get_by_role("searchbox", name="Submit").press("Enter")
    time.sleep(1)
    page.get_by_role("button", name="Принимаю").click(timeout=60000)
    page.get_by_role("link").filter(has_text=("Индивидуальный предприниматель")).click()

    data_1 = page.locator("div.col-md-12").filter(has_text='Основной вид деятельности').all_text_contents()
    page.get_by_role("link").filter(has_text="Все виды деятельности").click()
    time.sleep(1)
    page.evaluate("() => document.body.innerText")
    data_2 = page.get_by_text("Все виды деятельности Код Расшифровка").all_text_contents()
    data = []
    data.append(f'{data_2[0]} {data_1[0]}')
    for info in data:
        numeric_elements = re.findall(r'\d+\.\d+', info)
    return numeric_elements



    # ---------------------
    context.close()
    browser.close()


