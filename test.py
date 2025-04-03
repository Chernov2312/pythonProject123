import asyncio
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot.handlers.parse_to_exexl import create_excel_from_dict_list
import keyboard
from selenium.webdriver.support import expected_conditions as ec
from bot.handlers.parsing3 import parsing


def prokrut():
    itog = []
    url = "https://online.minjust.gov.kg/user/search?operator=AND&page=0&size=50"
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for i in range(810):
        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                f'/html/body/div[1]/div[3]/aside/div/div/form/div[8]')))
            k = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/aside/div/div/form/div[8]")
            k.click()
            actions = ActionChains(driver)
            actions.move_to_element(k).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            actions.send_keys(Keys.DOWN).perform()
            driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[{1}]").click()
            driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/aside/div/div/form/div[17]/div/button[2]").click()
            time.sleep(0.1)
            print(driver.current_url)
            parse = parsing(driver, driver.current_url)
            if len(parse) > 0:
                itog.extend(parse)

        except:
            pass

    for i in range(1, 12):
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/aside/div/div/form/div[8]").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[{1}]").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/aside/div/div/form/div[17]/div/button[2]").click()
        time.sleep(0.1)
        print(driver.current_url)
        parse = parsing(driver, driver.current_url)
        if len(parse) > 0:
            itog.extend(parse)
        time.sleep(0.5)
    driver.quit()
    print(itog)
    return  itog
create_excel_from_dict_list(prokrut(), "companies.xlsx")