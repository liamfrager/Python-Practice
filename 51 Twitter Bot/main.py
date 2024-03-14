from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time

load_dotenv
SPEED_TEST = "https://www.speedtest.net/"
TWITTER = "https://twitter.com/home?lang=en"
EMAIL = os.environ["TWITTER_EMAIL"]
PASSWORD = os.environ["TWITTER_PASSWORD"]


class InternetSpeedTwitterBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST)
        time.sleep(5)
        self.driver.find_element(
            By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a').click()
        time.sleep(60)
        dl = self.driver.find_element(
            By.CSS_SELECTOR, ".download-speed").text
        ul = self.driver.find_element(
            By.CSS_SELECTOR, ".upload-speed").text
        print(dl, ul)

    def tweet_at_provider(self):
        self.driver.get(TWITTER)
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sign in").click()
        email = self.driver.find_element(By.NAME, "text")
        email.send_keys(EMAIL, Keys.RETURN, PASSWORD)


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
# bot.tweet_at_provider()
