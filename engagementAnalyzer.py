from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import math

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
    likes = getLikes(driver)
    replies = getReplies(driver)
    retweets = getRetweets(driver)

    print(followers.text)
    print("---------------------")
    for like in likes:
        print(like.text)
    print("---------------------")
    for reply in replies:
        print(reply.text)
    print("---------------------")
    for retweet in retweets:
        print(retweet.text)

def getFollowers(driver):
    ### Store number of followers for later use
    val = driver.find_elements(By.XPATH, "//a[@role='link']")
    followers = val[8]

    return followers

def getReplies(driver):
    ### Get number of replies on loaded tweets
    replies = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")

    return replies

def getRetweets(driver):
    ### Get number of retweets on loaded tweets
    retweets = driver.find_elements(By.XPATH, "//div[@data-testid='retweet']")

    return retweets

def getLikes(driver):
    ### Get number of likes on loaded tweets
    likes = driver.find_elements(By.XPATH, "//div[@data-testid='like']")

    return likes

interactionChecker("elonmusk")