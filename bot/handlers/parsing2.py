import logging


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parsing():
    logging.basicConfig(level=logging.INFO)
    logging.info("парсер запущен")
    url = "https://online.minjust.gov.kg/user/search?fullNameRu=изи&operator=AND&page=0&size=50"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    companys = []
    for i in range(1, int(driver.find_element(By.XPATH, "/html/body/div/div[3]/main/div[1]/p").text.split()[0]) + 1):
        company = []
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
                    if s != " " and all(map(lambda x: x not in s, ["I", "V", "X"])) and (s != "1/2") and s.count(":") != 2 and not "(представительства)" in s:
                        if "== не заполнено ==" in s:
                            company.append("не заполненно")
                        else:
                            company.append(s)
                except:
                    pass
        company_2 = []
        rt = ""
        flag = False
        for j in range(2, len(company)):
            if "30. Учредители" in company[j - 1]:
                company_2.append(" ".join(rt.split()))
                rt = ""
                rt += ": " +company[j] + "\n"
                flag = True
            elif flag and company[j - 1].count(":") != 2 and company[j - 1].count("/") != 1:
                rt += company[j - 1] + "\n"
            elif len(company[j].split(". ")) >= 2:
                rt += ": " +company[j - 1]
                if "2. Полное наименование на официальном языке" in rt:
                    rt = "2. Полное наименование на официальном языке" +":" +" ".join(rt[len("2. Полное наименование на официальном языке"):].split(":"))
                rt = " ".join(rt.split())
                if rt.split(":")[0] == "":
                    rt = rt.split(":")[1]
                    continue
                company_2.append(rt)
                rt = ""
            else:
                rt += company[j - 1] + " "
        company_2.append(rt)
        for j in company_2:
            if any(list(map(lambda x: x.lower() in j.lower(),
                                    ["ИНН", "Телефон", "e-mail", "официальном языке", "Регистрационный номер",
                                     "Код ОКПО", "Область/город республиканского значения", "Район/город областного значения", "Город/село/поселок ",
                                     "Микрорайон/жилмассив", "Улица (проспект, бульвар, переулок и т.п.)", "№ дома",
                                     "№ квартиры (офиса, комнаты и т.п.)", "Факс",
                                     "Государственная регистрация или перерегистрация", "Дата приказа",
                                     "Дата первичной регистрации", "Форма собственности", "Фамилия, имя, отчество",
                                     "Основной вид деятельности", "Код экономической деятельности",
                                     "физических лиц", "юридических лиц", "Общее количество учредителей",
                                     "Учредители (участники)",
                                     "Учредитель (участник) Ф.И.О."]))):
                company_info[j.split(":")[0].strip()] = j.split(":")[1] if "== не заполнено ==" not in j.split(":")[1] else "не заполнено"
        last = company_info[list(company_info.keys())[-1]]
        del company_info[list(company_info.keys())[-1]]
        company_info["30. Учредители (участники)"] = " ".join(last.split("\n")[1:])[:-1:]
        for j in ['4. Сокращенное наименование на официальном языке', '7. Регистрационный номер', '8. Код ОКПО', '9. ИНН', '10. Область/город республиканского значения', '11. Район/город областного значения', '12. Город/село/поселок', '13. Микрорайон/жилмассив', '14. Улица (проспект, бульвар, переулок и т.п.)', '15. № дома', '16. № квартиры (офиса, комнаты и т.п.)', '17. Телефон', '18. Факс', '19. Электронный адрес (e-mail)', '20. Государственная регистрация или перерегистрация', '21. Дата приказа', '22. Дата первичной регистрации', '23. Форма собственности', '24. Фамилия, имя, отчество', '25. Основной вид деятельности', '26. Код экономической деятельности', '27. Количество учредителей (участников) - физических лиц', '28. Количество учредителей (участников) - юридических лиц', '29. Общее количество учредителей (участников)']:
            if j not in company_info:
                company_info[j] = "не заполнено"
        del company_info[list(company_info.keys())[0]]
        logging.info(f"{i},{company_info}")
        companys.append(company_info)
        if i % 50 == 0:
            url = f"https://online.minjust.gov.kg/user/search?fullNameRu=изи&operator=AND&page={i // 50}&size=50"
        driver.get(url)
    driver.quit()
    return companys

