import random
import webbrowser
import yaml
import requests
import time
import wget

def randDownloadTest():
    webList = []
    with open("resources/websites.txt") as webFile:
        for website in webFile:
            website = website.strip()       #get list of websites from text file into a list
            webList.append(website)

    randWeb = random.choice(webList)        #pick random website for user to access

    url = "https://" + randWeb          #add "https://" to make valid url 

    #userCreds = yaml.load(open("userCredentials.yaml"))
    #user1Email = userCreds['user1']['email']                #access yaml file info to make a user and fill out credentials for logging in
    #user1Passwd = userCreds['user1']['password']
    #print(user1Email, " ", user1Passwd)

    webbrowser.open_new_tab(url)            #open random website

    time.sleep(5)

    #--------Downloading files - V1

    url = "https://www.facebook.com/" 
    icon = "favicon.ico"

    webbrowser.open_new_tab(url)

    response = wget.download(url+icon, 'facebook1.ico')

    time.sleep(5)

    #--------Downloading files - V2

    url = "https://www.facebook.com/" 
    icon = "favicon.ico"

    webbrowser.open_new_tab(url)


    r = requests.get(url+icon, allow_redirects=True)

    open('facebook2.ico','wb').write(r.content)

    time.sleep(5)

    #--------Downloading large files

    url = "http://www.ece.rutgers.edu/undergraduate-and-graduate-student-handbooks" 

    webbrowser.open_new_tab(url)

    time.sleep(5)

    with open("handbook.pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
    
            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)