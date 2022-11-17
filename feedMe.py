from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import math

### Time between posts
### 86400 seconds is equivalent to 24 hours
timeInterval = 86400

with open('../info.txt', 'r') as reader:
    mylist = reader.read().splitlines() 

EMAIL = mylist[0]
USERNAME = mylist[1]
PASSWORD = mylist[2]

"""
TODO

Handle login errors such as activity warning popups
Basically just check that it's on the correct page

Make the sleep calls more sophisticated
i.e. make sure page is loaded, don't waste uneccesary time, etc.

More?????
"""

def main():
    driver = webdriver.Chrome()
    driver.get('http://twitter.com/i/flow/login')

    login(driver)

    time.sleep(5)

    ### Bot logged in, go to profile page rather than feed
    driver.find_element(By.XPATH, "//a[@aria-label='Profile']").click()

    time.sleep(5)

    checkStatus(driver)

def login(driver):
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']").send_keys(EMAIL)

    time.sleep(2)

    ### Get all the buttons on the page
    buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
    ### The 3rd button is the 'Next' button
    buttons[2].click()

    time.sleep(2)

    ### Not interactable????
    if(len(driver.find_elements(By.XPATH, "//span[text()='Phone or username']")) > 0):
        driver.find_element(By.XPATH, "//span[text()='Phone or username']").send_keys(USERNAME)

        buttons = driver.find_elements(By.XPATH, "//div[@role='button']")

        buttons[1].click()

    driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(PASSWORD)

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
    followers = val[8]

    followers = getFollowers(followers.text)

    ### Get number of replies on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")
    replies = val[1]

    ### Get number of retweets on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='retweet']")
    retweets = val[1]

    ### Get number of likes on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='like']")
    likes = val[1]

    getStatus(driver, int(followers.text), int(likes.text), int(replies.text), int(retweets.text))

def getStatus(driver, followers,  likes, replies, retweets):
    food = 0
    play = 0
    motivation = 0
    ### If like count met add 1 to food
    ### Else remove 1 to food
    ### Max of 7; if 0 then bot dies
    if(likes >= math.floor(followers * 0.2)):
        food = 1
    else:
        food = -1

    ### If reply count met add 1 to play
    ### Else remove 1 to play
    ### Max of 7; if 0 then bot dies
    if(replies >= math.floor(followers * 0.05)):
        play = 1
    else:
        play = -1

    ### If reply count met add 1 to motivation
    ### Else remove 1 to motivation
    ### Max of 7; if 0 then bot dies
    if(retweets >= math.floor(followers * 0.01)):
        motivation = 1
    else:
        motivation = -1

    updateStatus(driver, food, play, motivation)

### Update status file
def updateStatus(driver, food, play, motivation):

    with open('status.txt', 'r') as reader:
        statuses = reader.read().splitlines() 
    
    ### Status[0] is food
    statuses[0] = int(statuses[0]) + food

    ### Status[1] is play
    statuses[1] = int(statuses[1]) + play

    ### Status[2] is motivation
    statuses[2] = int(statuses[2]) + motivation

    for i in statuses:
        ### 7 is max satiety
        if(i > 7):
            i = 7
        ### 0 means bot has died
        if(i == 0):
            dead(driver)

    postPet(driver)

    with open('status.txt', 'w') as writer:
        for i in statuses:
            writer.write("%s\n" % i)

### RIP
### Print out dead pet and never run again
def dead(driver):
    driver.find_elements(By.XPATH, "//div[@data-block='true']").send_keys("I'm Dead!")

    driver.find_elements(By.XPATH, "//div[@data-testid='tweetButton']").click()

    ### Bot dead so end program
    exit()

### Post an ascii pet
### The ascii should be different depending
### on the level of food, play, and motivation
def postPet(driver):
    driver.find_elements(By.XPATH, "//div[@data-block='true']").send_keys("PUT ASCII ART HERE")

    driver.find_elements(By.XPATH, "//div[@data-testid='tweetButton']").click()

### Returns number of followers for the previous day
def getFollowers(followers):
    newFollowers = ""
    
    ### Get follower amount from previous day
    with open('followers.txt', 'r') as reader:
        newFollowers = reader.read()

    ### Write new follower count to file
    ### Will be utilized the next day
    with open('followers.txt', 'w') as writer:
        writer.write(followers)

    return newFollowers



if __name__ == "__main__":
    ### Do until bot dies
    while(True):
        main()
        time.sleep(timeInterval)
