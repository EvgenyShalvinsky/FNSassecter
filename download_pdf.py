import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, inn_text) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://egrul.nalog.ru/index.html")
    page.get_by_role("textbox", name="Поисковый запрос:*").click()
    page.get_by_role("textbox", name="Поисковый запрос:*").fill(f'{inn_text}')
    page.get_by_text("Выберите значения из справочника").click()
    page.get_by_text("</div></div></div></div>").content_frame.get_by_role("button", name="Выбрать все").click()
    page.get_by_text("</div></div></div></div>").content_frame.get_by_role("button", name="OK").click()
    page.get_by_role("button", name="Найти ").click()
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Получить выписку").click()
    download = download_info.value

    download.save_as(".//Data//test.pdf") #+ "download.suggested_filename")

    # ---------------------
    context.close()
    browser.close()


