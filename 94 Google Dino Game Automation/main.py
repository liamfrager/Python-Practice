from selenium import webdriver
from PIL import ImageGrab
import pyautogui as gui

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://chromedino.com/')
driver.maximize_window()
gui.click(400, 400)
gui.press('up')

jumps = 0
while True:
    game_over = ImageGrab.grab((820, 332, 850, 333)).convert('L').load()
    for i in range(30):
        if game_over[i, 0] < 100:
            gui.press('up')
            jumps = 0
            break

    # Not a great algorithm, but I tried.
    jump_if_obstacle_range = int(round(90 + jumps ** 1.7 * .1))
    jump_if_obstacle_range = jump_if_obstacle_range if jump_if_obstacle_range < 200 else 200
    screenshot = ImageGrab.grab(
        (610, 380, 610 + jump_if_obstacle_range, 400)
    ).convert('L').load()

    for i in range(jump_if_obstacle_range):
        top_pixel = screenshot[jump_if_obstacle_range - i - 1, 19]
        bot_pixel = screenshot[jump_if_obstacle_range - i - 1, 0]
        if top_pixel < 100 or bot_pixel < 100:
            gui.press('up')
            jumps += 1
            break


# HIGH SCORE: 1047
