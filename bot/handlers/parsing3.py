import asyncio
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def parsing(driver, url):
    # url = "https://online.minjust.gov.kg/user/search?fullNameRu=изи&operator=AND&page=0&size=50"
    # options = webdriver.ChromeOptions()
    # #options.add_argument("--headless")
    # #options.add_argument("--no-sandbox")
    # options.page_load_strategy = 'normal'
    # #options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=options)
    # driver.get(url)
    companys = []
    time.sleep(3)
    for i in range(1, int(driver.find_element(By.XPATH, "/html/body/div/div[3]/main/div[1]/p").text.split()[0]) + 1):
        logging.basicConfig(level=logging.INFO)
        company = []
        company_info = dict()
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            f"/html/body/div/div[3]/main/div[2]/div/div/div/div/div/div/table/tbody/tr[{50 if i % 50 == 0 else i % 50}]/td[8]/div")))
        driver.find_element(By.XPATH,
                            f"/html/body/div/div[3]/main/div[2]/div/div/div/div/div/div/table/tbody/tr[{50 if i % 50 == 0 else i % 50}]/td[8]/div").click()

        k = ""
        for u in range(1, 3):
            for j in range(80):
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    f'/html/body/div/div[3]/main/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[{1}]/div/div/div[2]/span[{1}]')))
                try:
                    s = driver.find_element(By.XPATH,
                                            f'/html/body/div/div[3]/main/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[{u}]/div/div/div[2]/span[{j + 1}]').text
                    if s != " " and all(map(lambda x: x not in s, ["I", "V", "X"])) and (s != "1/2") and s.count(
                            ":") != 2 and not "(представительства)" in s and (s != "2/2"):
                        if "== не заполнено ==" in s:
                            company.append("не заполненно")
                        else:
                            company.append(s)
                except:
                    pass
        value = ""
        key = ""
        for j in range(len(company)):
            if company[j].strip() == "языке" or company[j].strip() == "перерегистрация" or company[
                j].strip() == "юридических лиц" or company[j].strip() == "физических лиц":
                key += " " + company[j]
                continue
            if len(company[j]) >= 3 and (
                    company[j][0].isdigit() and company[j][1] == "." or company[j][0].isdigit() and company[j][
                1].isdigit() and company[j][2] == ".") and len(company[j].split(".")) != 3:
                if value == "":
                    value = "не заполнено"
                company_info[key] = value
                value = ""
                key = ""
            else:
                if "не заполнено" in company[j]:
                    value += "не заполнено"
                else:
                    value += company[j] + " "
            if len(company[j]) >= 3 and (
                    company[j][0].isdigit() and company[j][1] == "." or company[j][0].isdigit() and company[j][
                1].isdigit() and company[j][2] == "." and key == "") and len(company[j].split(".")) != 3:
                key = company[j]
        company_info[key] = value
        del company_info[""]
        companys.append(company_info)
        logging.info(f"{i}, {company_info}")
        if i % 50 == 0:
            url = "&".join(url.split("&")[:2]) +"&" +url.split("&")[2].split("=")[0] + f"={i//50}&" +url.split("&")[3]
        driver.get(url)
    return companys

# create_excel_from_dict_list(parsing(), "companies.xlsx")
