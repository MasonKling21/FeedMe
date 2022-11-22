from selenium import webdriver
from selenium.webdriver.common.by import By

import time

"""
TODO

Load 5 tweets no matter what

Store information somewhere so that repeated requests don't
need to be sent to the same accounts

"""

### An activity checker to analyze how much activity accounts get on average
def interactionChecker(accountName):
    driver = webdriver.Chrome()
    driver.get('http://twitter.com/' + accountName)

    time.sleep(5)

    followers = getFollowers(driver, accountName)
    getAccount(driver, accountName, followers)

    driver.quit()

def getFollowers(driver, accountName):
    ### Store number of followers for later use
    path = "//a[@href='/" + accountName + "/followers']"
    followers = driver.find_element(By.XPATH, path)

    print(followers.text)

    ### 117.5M Followers
    ### Get 117.5M and remove Followers
    followers = followers.text.split()

    return followers[0]

def getAccount(driver, accountName, followers):
    ### Get the poster so we can filter out retweets
    poster = driver.find_elements(By.XPATH, "//div[@data-testid='Tweet-User-Avatar']/../..")

    findUser = "//a[@href='/link']"
    findUser = findUser.replace("link", accountName)

    count = 0

    ### Finds the interaction on posts by account
    for post in poster:
        likes = post.find_element(By.XPATH, ".//div[@data-testid='like']")
        retweets = post.find_element(By.XPATH, "//div[@data-testid='retweet']")
        replies = driver.find_element(By.XPATH, "//div[@data-testid='reply']")
        
        getEngagementActivity(convert(likes.text),convert(retweets.text),convert(replies.text),convert(followers))
        count += 1

        if(count == 5):
            return

    return

def convert(num):
    ### Convert inputs into real numbers
    ### i.e 1M to 1000000 or 1.1k to 1100

    ### Remove commas from number
    num = num.replace(',', "")
    ### Make ending K or M lowercase
    num = num.lower()

    if num:
        mult = 1
        ### 1,000
        if num.endswith('k'):
            mult = 1000
            num = num[0:len(num)-1]
        ### 1,000,000
        elif num.endswith('m'):
            mult = 1000000
            num = num[0:len(num)-1]

    return int(float(num) * mult)

def getEngagementActivity(likes,retweets,replies,followers):

    print("Like Activity: " + f"{((likes / followers) * 100 ):.4f}" + "%")
    print("Reply Activity: " + f"{((replies / followers) * 100):.4f}" + "%")
    print("Retweet Activity: " + f"{((retweets / followers) * 100):.4f}" + "%")

interactionChecker("elonmusk")