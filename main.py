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

#import of secrets
import secrets



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
    if userType == "StoreAssistant":
        bookingLookUp()
        
def bookItems():
    print("test")
    
def bookingLookUp():
    print("test")
    
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

for i in secrets.username:
    user = i[0]
    userType = i[1]
    print(user)
    print(userType)
    load_time_testing(user, userType, passwordSecret)
    