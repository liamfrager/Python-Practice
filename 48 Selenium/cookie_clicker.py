from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

upgrades = ["Cursor", "Grandma", "Factory", "Mine",
            "Shipment", "Alchemy lab", "Portal", "Time machine"]
upgrade_costs = [
    int(driver.find_element(
        By.ID,
        f"buy{upgrade}"
    ).text.split("\n")[0].split(" - ")[1].replace(",", ""))
    for upgrade in upgrades
]

cookie = driver.find_element(By.ID, "cookie")
game_time = time.time() + 5 * 60


def play():
    try:
        while time.time() < game_time:
            timeout = time.time() + 3
            while time.time() < timeout:
                cookie.click()
            money = int(driver.find_element(
                By.ID, "money").text.replace(",", ""))
            for i in range(1, len(upgrade_costs) + 1):
                cost = upgrade_costs[-i]
                if money >= cost:
                    driver.find_element(By.ID, f"buy{upgrades[-i]}").click()
    except:
        print("exception!")
        play()


play()
cps = driver.find_element(By.ID, "cps").text
print(cps)
