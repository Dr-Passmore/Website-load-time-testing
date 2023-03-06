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
        bookItems(driver, user, userType)
    elif userType == "StoreAssistant":
        bookingLookUp(driver, user, userType)
    else:
        print("")
        
def bookItems():
    print("test bookItems")
    
def bookingLookUp(driver, user, userType):
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()

    time.sleep(0.5)

    booking_management = driver.find_element(By.CSS_SELECTOR, "[aria-label='Booking Management']")
    booking_management.click()

    time.sleep(shortDelay())
    # Wait for the element to be visible on the page
    wait = WebDriverWait(driver, 10)
    store_desk = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Store Desk")))

    # Move to the element and click on it
    actions = ActionChains(driver)
    actions.move_to_element(store_desk).perform()
    store_desk.click()

    time.sleep(shortDelay)
    test = user
    bookedto_search = driver.find_element(By.ID, "bookedto_search")
    for i in test:
        bookedto_search.send_keys(i)
    start = time.time()
    bookedto_search.send_keys(Keys.ENTER)
    bookedto_search.send_keys(Keys.PAGE_DOWN)

    wait = WebDriverWait(driver, 60)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sd-asset-item-content")))

    end = time.time()
    load_time_recorded = end-start
    
    #TODO cancel booking
    updateCSV(user, userType, load_time_recorded)
    
def updateCSV(user, userType, load_time_recorded):
    '''
    Writes new results to CSV output
    '''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = datetime.now().date()
    
    
    new_row = [current_date,
               current_time,
               user, 
               userType,
               load_time_recorded]
    
    with open("LoadingTimeResults.csv", "a", newline='') as csvFile:
        writer=csv.writer(csvFile)
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
    updateCSV(user, userType)
    