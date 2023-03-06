#selenium modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import of other python modules
import time
from random import randint
import logging
import os
import csv
from datetime import datetime

#import of secrets
import secrets
csvFile = './LoadingTimeResults.csv'



def load_time_testing(user, userType, passwordSecret):
    '''
    Initiates the webdriver and logs into the website
    '''
    logging.info(f"Starting test with {user}")
    driver = webdriver.Chrome()
    driver.get(secrets.target_url)
    driver.maximize_window()
    time.sleep(shortDelay())
    logging.info("login page")
    
    #input username
    username = driver.find_element(By.ID, "uname")
    for i in user:
        username.send_keys(i)
        time.sleep(0.1)
    time.sleep(1)

    #input password
    password = driver.find_element(By.ID, "pword")
    for i in passwordSecret:
        password.send_keys(i)
        time.sleep(0.1)
    time.sleep(1)

    #press login
    login = driver.find_element(By.ID, "login")
    login.click()
    logging.info("logged into system")
    time.sleep(longDelay())
    if userType == "Student":
        bookItems()
    elif userType == "StoreAssistant":
        bookingLookUp()
    else:
        print("")
        
def bookItems():
    print("test bookItems")
    
def bookingLookUp():
    print("test")
    
def updateCSV():
    new_row = ["test", 
               "test2"]
        
    with open("LoadingTimeResults.csv", "a", newline='') as csvFile:
        writer=csv.writer(csvFile)
        #csvFile.write("\n")
        writer.writerow(new_row)
    csvFile.close()

    
def longDelay():
    '''
    Provides a random delay between 3 and 7 seconds
    '''
    return randint(3,7)

def shortDelay():
    '''
    Provides a random delay between 1 and 3 seconds
    '''
    return randint(1, 3)

passwordSecret = secrets.password

logging.basicConfig(filename='testing.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

for i in secrets.username:
    user = i[0]
    userType = i[1]
    #load_time_testing(user, userType, passwordSecret)
    updateCSV()
    