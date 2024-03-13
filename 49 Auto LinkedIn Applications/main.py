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


jobs = driver.find_elements(By.CLASS_NAME, "job-card-container")

with open('jobs.txt', mode='a') as file:
    for job in jobs:
        job = job.text.split("\n")
        new_job = {}
        new_job["title"] = job[0] if len(job) > 0 else None,
        new_job["company"] = job[1] if len(job) > 1 else None,
        new_job["location"] = job[2] if len(job) > 2 else None,
        new_job["salary"] = job[3] if len(job) > 3 else None,
        file.write(f"{new_job}\n")
driver.quit()
