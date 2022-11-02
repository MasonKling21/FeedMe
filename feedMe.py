from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time



driver = webdriver.Chrome()
driver.get('http://twitter.com/i/flow/login')

time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys('USERNAME')

time.sleep(2)

buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
buttons[2].click()

time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys('PASSWORD')

time.sleep(2)

buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
buttons[2].click()

time.sleep(2)