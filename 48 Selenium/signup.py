from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://secure-retreat-92358.herokuapp.com/")

# # By finding each element
# form_data = [
#     {"name": "fName", "value": "Liam"},
#     {"name": "lName", "value": "Frager"},
#     {"name": "email", "value": "liam.frager@gmail.com"}
# ]

# for data in form_data:
#     input = driver.find_element(By.NAME, data["name"])
#     input.send_keys(data["value"])

# With key inputs
input = driver.find_element(By.NAME, "fName")
input.send_keys("Liam", Keys.TAB, "Frager", Keys.TAB,
                "liam.frager@gmail.com", Keys.TAB, Keys.ENTER)


driver.find_element(By.CSS_SELECTOR, "button").click()
