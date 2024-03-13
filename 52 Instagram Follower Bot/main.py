from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time

load_dotenv()
INSTA_USERNAME = os.environ["INSTAGRAM_USERNAME"]
INSTA_PW = os.environ["INSTAGRAM_PASSWORD"]
USER = "_catben_"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(f"https://www.instagram.com/{USER}")
time.sleep(1)


class InstaFollower():
    def login(self):
        username = driver.find_element(
            By.CSS_SELECTOR, "input[name='username']")
        username.send_keys(INSTA_USERNAME, Keys.TAB, INSTA_PW)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)

    def search_account(self, account):
        driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Search']").click()
        search = driver.find_element(By.CSS_SELECTOR, "input")
        search.send_keys(account, Keys.TAB, Keys.TAB, Keys.ENTER)
        time.sleep(6)

    def follow_all_followers(self, account):
        self.search_account(account)
        driver.find_element(By.PARTIAL_LINK_TEXT, "followers").click()
        time.sleep(2)
        ActionChains(driver).send_keys(
            Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB).perform()

        for _ in range(29):
            time.sleep(1)
            ActionChains(driver).send_keys(
                Keys.ENTER, Keys.TAB, Keys.TAB, Keys.TAB).perform()


bot = InstaFollower()
bot.login()
bot.follow_all_followers(USER)
