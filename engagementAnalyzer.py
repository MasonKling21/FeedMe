from selenium import webdriver
from selenium.webdriver.common.by import By

import time

"""
TODO

Load 5 tweets no matter what

Store information somewhere so that repeated requests don't
need to be sent to the same accounts

Handle numbers with commas
i.e: 1,000 turns to 1000

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

    ### 117.5M Followers
    ### Get 117.5M and remove Followers
    followers = followers.text.split()

    return followers[0]

def getAccount(driver, accountName, followers):
    ### Get the poster so we can filter out retweets
    poster = driver.find_elements(By.XPATH, "//div[@data-testid='Tweet-User-Avatar']/../..")

    findUser = "//a[@href='/link']"
    findUser = findUser.replace("link", accountName)

    ### Finds the interaction on posts by account
    for post in poster:
        likes = post.find_element(By.XPATH, ".//div[@data-testid='like']")
        retweets = post.find_element(By.XPATH, "//div[@data-testid='retweet']")
        replies = driver.find_element(By.XPATH, "//div[@data-testid='reply']")

        getEngagementActivity(convert(likes.text),convert(retweets.text),convert(replies.text),convert(followers))

    return

def convert(num):
    ### Convert inputs into real numbers
    ### i.e 1M to 1000000 or 1.1k to 1100
    if num:
        mult = 1
        ### 1,000
        if num.endswith('K'):
            mult = 1000
            num = num[0:len(num)-1]
        ### 1,000,000
        elif num.endswith('M'):
            mult = 1000000
            num = num[0:len(num)-1]

    return int(float(num) * mult)

def getEngagementActivity(likes,retweets,replies,followers):

    print("Like Activity: " + likes / followers)
    print("Reply Activity: " + replies / followers)
    print("Retweet Activity" + retweets / followers)

interactionChecker("elonmusk")