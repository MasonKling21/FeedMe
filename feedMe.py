from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

def main():
    driver = webdriver.Chrome()
    driver.get('http://twitter.com/i/flow/login')

    login(driver)

    time.sleep(2)

    checkStatus(driver)

def login(driver):
    driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys('USERNAME')

    time.sleep(2)

    ### Get all the buttons on the page
    buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
    ### The 3rd button is the 'Next' button
    buttons[2].click()

    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys('PASSWORD')

    time.sleep(2)

    ### Get all the buttons on the page
    buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
    ### The 3rd button is the 'Login' button
    buttons[2].click()

### Compares the number of likes, comments, and retweets of the most
### recent post against the amount of followers at the time of the post
def checkStatus(driver):

    ### Give page some time to load
    time.sleep(10)

    ### Get number of followers
    ### Store number of followers for later use
    val = driver.find_elements(By.XPATH, "//a[@role='link']")

    ### Get number of replies on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")

    ### Get number of retweets on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='retweet']")

    ### Get number of likes on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='like']")




if __name__ == "__main__":
    main()
