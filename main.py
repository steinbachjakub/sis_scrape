"""
Script to scrape data from student.vscht.cz
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd


LOGIN = "steinbaj"
PASSWORD = "Sedlcanska 18 Praha"

results = []

with webdriver.Chrome() as driver:
    driver.get("https://student.vscht.cz")
    input_login = driver.find_element(By.XPATH, "//input[@id='login']")
    input_login.send_keys(LOGIN)
    input_password = driver.find_element(By.XPATH, "//input[@id='heslo']")
    input_password.send_keys(PASSWORD)
    input_password.send_keys(Keys.ENTER)
    # # sleep(0.5)
    link_change_role = driver.find_element(By.XPATH, "//a[@title='výběr role']")
    link_change_role.click()
    link_role_umat = driver.find_element(By.XPATH, "//a[@class='link2']")
    link_role_umat.click()
    link_grupik = driver.find_element(By.XPATH, '//a[@id="hint_grupik"]')
    link_grupik.click()
    link_grupik_mat = driver.find_element(By.XPATH, '//a[text()="St 12:00 C13, Čt 15:00 B22"]')
    link_grupik_mat.click()
    links_study_groups = driver.find_elements(By.XPATH, "//tr[@class='row5']/td/a[contains (@href, '22aB413001')]")

    for i in range(1):
        links_study_groups = driver.find_elements(By.XPATH, "//tr[@class='row5']/td/a[contains (@href, '22aB413001')]")
        links_study_groups[i].click()
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table_info = soup.find("div", text="Informace o skupině").parent
        teacher = table_info.find("th", text="Vyučující:  ").parent.find("td").text
        program = soup.find("table", id="table_seznam").find_all("tr")[1].find_all("td")[2].text
        table_results = soup.find("table", id="table_seznam")
        test_1 = []
        test_2 = []

        for row in table_results.find_all("tr")[1:-1]:
            test_1.append(row.find_all("td")[4].text)
            test_2.append(row.find_all("td")[5].text)

        results.append({
            "teacher": teacher,
            "group": program,
            "test_1": test_1,
            "test_2": test_2
        })
    print(results)
    sleep(2)



