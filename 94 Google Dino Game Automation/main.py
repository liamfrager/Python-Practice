from selenium import webdriver
from PIL import ImageGrab
import pyautogui as gui
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://chromedino.com/')
driver.maximize_window()
gui.click(400, 400)
gui.press('up')
# gui.mouseInfo()

jumps = 0
while True:
    # time.sleep(.01)
    area = ImageGrab.grab((650, 380, 800, 400)).convert('L')
    pixels = area.load()

    for i in range(50 + jumps if 50 + jumps < 70 else 70):
        top_pixel = pixels[i, 19]
        bot_pixel = pixels[i, 0]
        if top_pixel < 100 or bot_pixel < 100:
            gui.press('up')
            jumps += 1
            break


driver.quit()
