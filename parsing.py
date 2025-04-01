import logging

from bs4 import BeautifulSoup
import pdfplumber
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parsing():
    logging.basicConfig(level=logging.INFO)
    url = "https://online.minjust.gov.kg/user/search?fullNameRu=изи&operator=AND&page=0&size=50"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    company = []
    for i in range(1, int(driver.find_element(By.XPATH, "/html/body/div/div[3]/main/div[1]/p").text.split()[0]) + 1):
        company_info = dict()
        time.sleep(2.5)
        driver.find_element(By.XPATH,
                            f"/html/body/div/div[3]/main/div[2]/div/div/div/div/div/div/table/tbody/tr[{50 if i % 50 == 0 else i % 50}]/td[8]/div").click()

        time.sleep(2.5)
        k = ""
        for u in range(1, 3):
            for j in range(80):
                try:
                    s = driver.find_element(By.XPATH,
                                            f'/html/body/div/div[3]/main/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[{u}]/div/div/div[2]/span[{j + 1}]').text
                    if k and s != " " and s != "Учредитель (участник) Ф.И.О." and s:
                        company_info[" ".join(k.split(". ")[1:])] += s if not "III" in s and not "IV" in s and not "Организационно-правовая форма" in s and not "== не заполнено ==" in s else "не заполнено"
                        k = ""
                    if any(list(map(lambda x: x.lower() in s.lower(),
                                    ["ИНН", "Телефон", "e-mail", "официальном языке", "Регистрационный номер",
                                     "Код ОКПО", "Область/город республиканского значения", "Район/город областного значения", "Город/село/поселок ",
                                     "Микрорайон/жилмассив", "Улица (проспект, бульвар, переулок и т.п.)", "№ дома",
                                     "№ квартиры (офиса, комнаты и т.п.)", "Факс",
                                     "Государственная регистрация или перерегистрация", "Дата приказа",
                                     "Дата первичной регистрации", "Форма собственности", "Фамилия, имя, отчество",
                                     "Основной вид деятельности", "Код экономической деятельности",
                                     "физических лиц", "юридических лиц", "Общее количество учредителей",
                                     "Учредители (участники)",
                                     "Учредитель (участник) Ф.И.О."]))) and not "III" in s and not "IV" in s and s:
                        k = s
                except:
                    pass
        for j in ['Полное наименование на официальном языке', 'Регистрационный номер', 'Код ОКПО', 'ИНН',
                  'Область/город республиканского значения', 'Район/город областного значения', 'Микрорайон/жилмассив',
                  'Улица (проспект, бульвар, переулок и т.п.)', '№ дома', '№ квартиры (офиса, комнаты и т.п.)',
                  'Телефон', 'Факс', 'Электронный адрес (e-mail)', 'Дата приказа', 'Дата первичной регистрации',
                  'Форма собственности', 'Фамилия, имя, отчество', 'Основной вид деятельности',
                  'Код экономической деятельности', 'Общее количество учредителей (участников)',
                  'Учредители (участники):']:
            if j not in company_info:
                company_info[j] = "не заполнено"
        company.append(company_info)
        logging.info(f"{i}, {company_info}")
        if i == 4:
            break
        if i % 50 == 0:
            url = f"https://online.minjust.gov.kg/user/search?fullNameRu=изи&operator=AND&page={i // 50}&size=50"
            break
        driver.get(url)
    driver.quit()
    return company
