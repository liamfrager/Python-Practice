from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.environ["TINDER_EMAIL"]
PASSWORD = os.environ["TINDER_PASSWORD"]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://tinder.com/")
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Log in").click()
time.sleep(2)
driver.find_element(
    By.XPATH, '/html/body/div[2]/main/div[1]/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button').click()
time.sleep(2)

driver.switch_to.window(driver.window_handles[1])

login_form = driver.find_element(By.XPATH, '//*[@id="email"]')
login_form.send_keys(EMAIL, Keys.TAB, PASSWORD, Keys.TAB, Keys.ENTER)

driver.switch_to.window(driver.window_handles[0])
time.sleep(5)
driver.find_element(
    By.XPATH, '/html/body/div[2]/main/div[1]/div/div/div[3]/button[1]').click()
time.sleep(1)
driver.find_element(
    By.XPATH, '/html/body/div[2]/main/div[1]/div/div/div[3]/button[2]').click()

time.sleep(10)
ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
for _ in range(500):
    try:
        driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[2]/div/div/div[1]/div[1]/div/div[4]/div/div[2]/button').click()
    except (NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException):
        try:
            driver.find_element(
                By.XPATH, '/html/body/div[2]/main/div[1]/div[2]/button[2]').click()
        except:
            pass
    time.sleep(1)
