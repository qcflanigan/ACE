from random import randint
import random
from selenium import webdriver
import yaml
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def staticWebsiteTest():
    webList = []
    with open("websites.txt") as webFile:
        for website in webFile:
            website = website.strip()       #get list of websites from text file into a list
            webList.append(website)


    randWeb = random.choice(webList)        #pick random website for user to access

    url = "https://" + randWeb + ".com"      #add "https://" to make valid url 

    userCreds = yaml.load(open("webCredentials.yaml"))
    googleButton = userCreds[randWeb]['class_name']                #access yaml file info to access the random page's button to click

    driver = webdriver.Firefox()        #make instance of a web driver to access random websites on firefox

    driver.get(url)         #go to randomly chosen url
    #driver.maximize_window()
    driver.maximize_window()

    web_button = driver.find_element(By.CSS_SELECTOR, googleButton)  
    time.sleep(2)


    web_button.click()

    time.sleep(5)

    driver.close()
    ebList = []
    with open("websites.txt") as webFile:
        for website in webFile:
            website = website.strip()       #get list of websites from text file into a list
            webList.append(website)


    randWeb = random.choice(webList)        #pick random website for user to access

    url = "https://" + randWeb + ".com"      #add "https://" to make valid url 

    userCreds = yaml.load(open("webCredentials.yaml"))
    googleButton = userCreds[randWeb]['class_name']                #access yaml file info to access the random page's button to click

    driver = webdriver.Firefox()        #make instance of a web driver to access random websites on firefox

    driver.get(url)         #go to randomly chosen url
    #driver.maximize_window()
    driver.maximize_window()

    web_button = driver.find_element(By.CSS_SELECTOR, googleButton)  
    time.sleep(2)


    web_button.click()

    time.sleep(5)

    driver.close()