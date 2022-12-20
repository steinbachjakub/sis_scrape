"""
Script to scrape data from student.vscht.cz
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re


LOGIN = "steinbaj"
PASSWORD = "Sedlcanska 18 Praha"

results = pd.DataFrame(
    {"Obor": [],
     "1. PP": [],
     "2. PP": [],
     "Vyučující": []}
)

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

    for i in range(len(links_study_groups)):
    # for i in range(40, 41):
        links_study_groups = driver.find_elements(By.XPATH, "//tr[@class='row5']/td/a[contains (@href, '22aB413001')]")
        links_study_groups[i].click()
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        table_info = soup.find("div", text="Informace o skupině").parent
        teacher_text = table_info.find("th", text="Vyučující:  ").parent.find("td").text.replace(u'\xa0', u' ')
        m = re.search(r"\).*\(", teacher_text)
        if m:
            teacher = m.group(0)[1:-2]
        else:
            teacher = teacher_text[:teacher_text.find("(") - 1]
        program = soup.find("table", id="table_seznam").find_all("tr")[1].find_all("td")[2].text.replace(u'\xa0', u'')
        table_results = soup.find("table", id="table_seznam")
        with open("temp_file.html", "w", encoding="utf-16") as f:
            f.write(str(table_results))
        df = pd.read_html("temp_file.html", header=0)[0][["Obor", "1. PP", "2. PP"]].iloc[:-1, :]
        df["Vyučující"] = teacher
        results = pd.concat([results, df])

    results.to_csv("data.csv", index=False)




