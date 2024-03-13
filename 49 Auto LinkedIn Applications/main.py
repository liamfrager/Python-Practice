from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time

load_dotenv()
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3845721496&distance=25&f_E=1%2C2&f_WT=2&geoId=103644278&keywords=junior%20web%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

time.sleep(1)
driver.find_element(By.LINK_TEXT, "Sign in").click()
time.sleep(1)
input = driver.find_element(By.ID, "username")
input.click()
input.send_keys(EMAIL, Keys.TAB, PASSWORD)
submit = driver.find_element(
    By.CSS_SELECTOR, ".login__form_action_container button").click()
time.sleep(3)


jobs = [driver.find_element(
    By.XPATH, f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[{i+1}]/div/div/div/div[2]") for i in range(25)]
jobs = [
    job.find_elements(By.XPATH, ".//div").text
    for job in jobs
]
print(jobs)
all_jobs = []
for job in jobs:
    pass

time.sleep(1000)
driver.quit()
