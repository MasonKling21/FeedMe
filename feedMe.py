from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import math

"""
TODO

Ensure that path is right after login

Add posting functionality

Create art to make the bot feel alive

More?????
"""

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
    followers = val[8]

    followers = getFollowers(str(followers))

    ### Get number of replies on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")
    replies = val[1]

    ### Get number of retweets on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='retweet']")
    retweets = val[1]

    ### Get number of likes on last tweet
    val = driver.find_elements(By.XPATH, "//div[@data-testid='like']")
    likes = val[1]

    getStatus(followers, likes, replies, retweets)

def getStatus(followers,  likes, replies, retweets):
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

    updateStatus(food, play, motivation)

### Update status file
def updateStatus(food, play, motivation):
    foodStatus = 0
    playStatus = 0
    motivationStatus = 0

    with open('status.txt', 'r') as reader:
        foodStatus = reader.readline()
        playStatus = reader.readline()
        motivationStatus = reader.readline()
    
    foodStatus = int(foodStatus) + food
    playStatus = int(playStatus) + play
    motivationStatus = int(motivationStatus) + motivation

    if(foodStatus > 7):
        foodStatus = 7
    if(playStatus > 7):
        playStatus = 7
    if(motivationStatus > 7):
        motivationStatus = 7

    if(foodStatus == 0 or playStatus == 0 or motivationStatus == 0):
        dead()

    postPet()
    
    statuses = [str(foodStatus) + "\n", str(playStatus) + "\n", str(motivationStatus) + "\n"]

    with open('status.txt', 'w') as writer:
        writer.writelines(statuses)

### RIP
### Print out dead pet and never run again
def dead():
    print("I'm dead")

### Post an ascii pet
### The ascii should be different depending
### on the level of food, play, and motivation
def postPet():
    print("Pet")

### Returns number of followers for the previous day
def getFollowers(followers):
    newFollowers = ""
    
    with open('followers.txt', 'r') as reader:
        newFollowers = reader.read()

    with open('followers.txt', 'w') as writer:
        writer.write(followers)

    return newFollowers



if __name__ == "__main__":
    updateStatus(-1, -1, 1)
