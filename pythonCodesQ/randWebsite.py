from random import randint
import random
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

#import yaml - might need if we read in web elements statically, want to do randomly for now


def getLinkCoordinates(pathLink):       #function that returns x, y coordinates of a specific web element
    height = pathLink.size['height']
    width = pathLink.size['width']
    return width, height

def hasSize(link):       #function to check if a link element has any size, use to limit number of clickable links
    if link.size['height']>0 and link.size['width']>0:     #accessing height and width of size dictionary, check both to make compatable with '>'
        return True
    else:
        return False

def getRandInt():               #returns random integer from [1, 2], used to make web nav more random, user-like
    waitTime = random.randint(1, 2)
    return waitTime

def getRandScrollSpeed():           #returns random int from [5, 16] to scroll down page at random speed, simulate user access
    randScrollSpeed = random.randint(5, 16)     #5-very slow, 16-pretty fast. trying to stay in the speed range of a normal user
    return randScrollSpeed


#good for now, scrolls smoothly and randomly, try to scroll to a place and pick a link from there?
    #currently picks a link from the page then scrolls to random location based on the y coordinate for that link
def scrollToElement(driver, speed, pathLink):          #function to scroll down the page, sim user activity of scrolling down a page+choosing element
        x, y = getLinkCoordinates(pathLink)     #get web element's coordinates for scrolling
        pageHeight = driver.execute_script("return document.body.scrollHeight")//1.2
        minHeight = pageHeight//20
        if pageHeight<=100:     #getting rid of randrange() errors, making sure pageHeight > minHeight always 
            minHeight=0
        randHeight = random.randint(minHeight, pageHeight)      #pick a scroll length between 300 and the height of the page (scrolling to bottom of page)
        currPos, scrollHeight = 0, 1        #just to initialize the loop
        while currPos <= scrollHeight:      #loop to scroll smoothly
            currPos+=speed                  #scroll speed is random  variable, controls how fast we scroll with .format()
            driver.execute_script("window.scrollTo(0, {});".format(currPos))          #scroll with speed being updated each iteration
            scrollHeight = y+randHeight         #set scrollHeight to be the Y coordinate of the web element + a random value so we see the scrolling


def getVisibleLinks(pathLinks):     #function to sort through all links on a page and find the accessible ones
    visibleLinks = []
    for link in pathLinks:
        if link.is_displayed() and link.is_enabled():       #if link is in view of driver, has size>0 and clickable, add it to be visibileLinks list
            if hasSize(link):
                visibleLinks.append(link)
    return visibleLinks

def randWebsite():

    webList = []
    with open("websites.txt") as webFile:
        for website in webFile:
            website = website.strip()       #get list of websites from text file into a list
            webList.append(website)


    randWeb = random.choice(webList)        #pick random website for user to access
    print(randWeb)

    url = "https://" + randWeb      #add "https://" to make valid url 

    # userCreds = yaml.load(open("webCredentials.yaml"))
    # googleButton = userCreds[randWeb]['class_name']                #access yaml file info to access the random page's button to click
    # c_options = webdriver.ChromeOptions()
    # c_options.add_experimental_option("useAutomationExtension", False)            #get rid of chrome flag alerting of automation software
    # c_options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome()        #instance of a web driver to access random websites on chrome

    driver.get(url)         #go to randomly chosen url
    driver.maximize_window()        #full screen to have more space to find links

    time.sleep(getRandInt())      #wait for random num of seconds to see effects of buttons before continuing on path

    tab_is_open = True
    while tab_is_open:                  #loop to naviagte down a path on the same website
        print("entering while loop\n")
    
        driver.implicitly_wait(3)

        pathLinks = driver.find_elements(By.PARTIAL_LINK_TEXT, "")      #tag_name finds all links available on page, builds list of all website links to choose one randomly
        print("got list of links\n")

        visibleLinks = getVisibleLinks(pathLinks)                      #sorting through all links to only get clickable ones
        print("got visible links\n")

        if len(visibleLinks)==0:           #if no visible links on page, close program -> FOR FUTURE -> maybe we could navigate to a new random website?
            time.sleep(3)
            driver.close()
            exit(0)

        pathLink = visibleLinks[randint(0, len(visibleLinks)-1)]        #choose random link from visible links
        print("got link\n")
        driver.implicitly_wait(3)       #giving time for driver+page to load before advancing   

        scrollSpeed = getRandScrollSpeed()      #use random int function to create a random speed for scrolling down page
        print("scrolling\n")
        scrollToElement(driver, scrollSpeed, pathLink)       #scroll down to random web element (pathLink)
        time.sleep(1)

        print("about to click\n")
        driver.execute_script("arguments[0].click();", pathLink)       #sub for pathLink.click(), fixes "elememt would be intercepted" error
        

        print("clicked on new link\n")
        time.sleep(getRandInt())
        pathLinks.clear()       #clear array of links before next loop iteration (redundant?)
        visibleLinks.clear()

        print("checking quitNum\n")
        quitNum = randint(0, 15)
        if quitNum==0:                              #exits loop randomly, when randint() == 0
            tab_is_open=False
            time.sleep(1)
            print("quitNum: ", quitNum)
            break


    driver.implicitly_wait(2)       #stay on page for 2 seconds, then close tab

    driver.close()    #close web driver
