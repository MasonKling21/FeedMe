from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import math
import re

"""
TODO

Ensure the tweet isn't a comment or a retweets
If the tweet isn't a top level tweet will have to load more tweets
because I want there to be at least 5 tweets analyzed per account

Store information somewhere so that repeated requests don't
need to be sent to the same accounts

Will need to remove the letter value at the end of number larger than 1,000
i.e: 1K and 1M

"""

### An activity checker to analyze how much activity accounts get on average
def interactionChecker(accountName):
    driver = webdriver.Chrome()
    driver.get('http://twitter.com/' + accountName)

    time.sleep(5)

    followers = getFollowers(driver)
    poster = getAccount(driver, accountName, followers)

def getFollowers(driver):
    ### Store number of followers for later use
    val = driver.find_elements(By.XPATH, "//a[@role='link']")
    followers = val[8]

    return followers

def getAccount(driver, accountName, followers):
    ### Get the poster so we can filter out retweets
    poster = driver.find_elements(By.XPATH, "//div[@data-testid='Tweet-User-Avatar']/../..")

    findUser = "//a[@href='/link']"
    findUser = findUser.replace("link", accountName)

    ### Finds the interaction on posts by account
    for post in poster:
        likes = post.find_element(By.XPATH, ".//div[@data-testid='like']")
        retweets = post.find_elements(By.XPATH, "//div[@data-testid='retweet']")
        replies = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")

        getEngagementActivity(likes,retweets,replies,followers)

    return

def getEngagementActivity(likes,retweets,replies,followers):
    ### Convert inputs into real numbers
    ### i.e 1M to 1000000 or 1k to 1000

    print("Like Activity: " + likes / followers)
    print("Reply Activity: " + replies / followers)
    print("Retweet Activity" + retweets / followers)

interactionChecker("elonmusk")