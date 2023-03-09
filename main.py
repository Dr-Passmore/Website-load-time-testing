#selenium modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

#import of other python modules
import time
from random import randint
import logging
import csv
from datetime import datetime
import datetime as dt
from timeit import default_timer as timer

#import of secrets
import secrets
csvFile = './LoadingTimeResults.csv'




def load_time_testing(user, userType, passwordSecret, item):
    '''
    Initiates the webdriver and logs into the website
    '''
    logging.info(f"Starting test with {user}")
    driver = webdriver.Chrome()
    #Sets wait time to 5 minutes for page element to load
    wait = WebDriverWait(driver, 300)
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
    start = timer()
    process = "Login to Dashboard"
    login = driver.find_element(By.ID, "login")
    login.click()
    if userType == "Admin":
        wait.until(EC.visibility_of_element_located((By.ID, "form_panel_icons")))
    else:     
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dashboard-outer-wrapper")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info("logged into system")
    time.sleep(longDelay())
    if userType == "Student":
        bookItems(driver, wait, user, userType, item)
    elif userType == "StoreAssistant":
        bookingLookUp(driver, wait, user, userType)
    else:
        print("admin")
        driver.quit()
        
def bookItems(driver, wait, user, userType, item):
    #user accounts will book items following the key 
    booking = driver.find_element(By.LINK_TEXT, "Book")
    booking.click()
    
    time.sleep(shortDelay())
    
    #Selects "By items"
    booking_item = driver.find_element(By.ID, "basket-title")
    booking_item.click()
    
    time.sleep(longDelay())
    
    #Search menu - typing in the item
    booking_searchbar = driver.find_element(By.ID, "asearch")
    for i in item:
        booking_searchbar.send_keys(i)
        time.sleep(0.1)
    
    #hitting enter timing search
    process = "Search for item"
    start = timer()
    booking_searchbar.send_keys(Keys.ENTER)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "asset-item")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info("Search completed")
    
    time.sleep(shortDelay())
    
    #Timing until item becomes bookable
    process = f"{item} look up time"
    start = timer()
    book_item = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Add to Basket']")))
    book_item.click()
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info(f"{item} selected for booking")
  
    time.sleep(shortDelay())
    
    #Moving to the basket
    basket = driver.find_element(By.CSS_SELECTOR, "[aria-label='Basket']")
    process = "Basket load time"
    start = timer()
    basket.click()
    select_start_date = wait.until(EC.visibility_of_element_located((By.ID, "dtp_collection_log")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    #select_start_date = driver.find_element(By.ID, "dtp_collection_log")
    #Select collection
    select_start_date.click()
    logging.info(f"basket has loaded after {load_time_recorded} seconds")
    
    time.sleep(shortDelay())
    
    
    select_friday = dateSelection()
    select_date = driver.find_element(By.CSS_SELECTOR, f"[aria-label='{select_friday}']")
    select_date.click()
    
    time.sleep(shortDelay())
    
    # Find the dropdown element
    select_time = Select(driver.find_element(By.ID, "collection-time"))

    time.sleep(shortDelay())
    # Select the option with value "11:00:00"
    select_time.select_by_value("11:00:00")
    
    time.sleep(longDelay())
    
    next = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next']")
    next.click()
    
    time.sleep(shortDelay())
    
    select_end_date = driver.find_element(By.ID, "dtp_return_log")
    select_end_date.click()
    
    time.sleep(longDelay())
    
    
    print (dateSelection())
    
    return_date = driver.find_element(By.ID, "return-overlay")
    select_return_date = return_date.find_element(By.CSS_SELECTOR, f"[aria-label='{select_friday}']")
    select_return_date.click()
    
    #time.sleep(10)
    time.sleep(longDelay())
    
    # Find the dropdown element
    select_time = Select(driver.find_element(By.ID, "return-time"))

    # Select the option with value "11:00:00"
    select_time.select_by_value("11:45:00")
    
    time.sleep(shortDelay())
    
    
    #nextReturn = select_start_date.find_element(By.XPATH, "./following-sibling::div[@id='dtp_return_log']")
    nextReturn = return_date.find_element(By.CSS_SELECTOR, "[aria-label='Next']")
    #nextReturn = driver.find_element(By.CLASS_NAME, "form-button")
    
    process = "Return date and Time Selected"
    start = timer()
    nextReturn.click()
    check_avalibility = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Check Availability']")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info(f"Return date and Time Selected after {load_time_recorded}")
    
    time.sleep(shortDelay())
    
    
    process = "Avalibility Check"
    start = timer()
    check_avalibility.click()
    booking = wait.until(EC.visibility_of_element_located((By.ID, "basket-review-content"))) 
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info("Avalibility check completed")
    
    time.sleep(longDelay())
    
    basket_booking = booking.find_element(By.CSS_SELECTOR, "[aria-label='Book']")
    
    process = "Booking made"
    start = timer()
    basket_booking.click()
    
     
    #terms_toggle = driver.find_element(By.CSS_SELECTOR, "label[for='basket_terms']")
    terms_toggle = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='basket_terms']")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded)
    logging.info("Booking form loaded")
    terms_toggle.click()
    
    time.sleep(shortDelay())
    
    
    booking_form = driver.find_element(By.ID, "basket-form-content")
    book = booking_form.find_element(By.CSS_SELECTOR, "[aria-label='Book']")
    book.click()
    
    time.sleep(longDelay())
    
    #updateCSV(user, userType, load_time_recorded)
    
    print("order completed")
    
    driver.quit()
    
def bookingLookUp(driver, wait, user, userType):
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()

    time.sleep(shortDelay())

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

    time.sleep(shortDelay())
    test = "testinggamesstudent@test.ac.uk"
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
    
def updateCSV(user, userType, process, load_time_recorded):
    '''
    Writes new results to CSV output
    '''
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = datetime.now().date()
    
    logging.info("Updating CSV file")
    
    new_row = [current_date,
               current_time,
               user, 
               userType,
               process,
               load_time_recorded]
    
    with open("LoadingTimeResults.csv", "a", newline='') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(new_row)
    csvFile.close()
    logging.info(f"CSV updated with {new_row}")

    
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

def dateSelection():
    # Get today's date
    currentday = dt.date.today()

    # Calculate the next Friday
    friday = currentday + dt.timedelta((4 - currentday.weekday()) % 7 + 7)

    # Format the date as "Fri, Mar 17th 2023"
    friday_str = friday.strftime("%a, %b %d")

    # Add "st", "nd", "rd", or "th" to the day based on its value
    if friday.day in [1, 21, 31]:
        friday_str += "st"
    elif friday.day in [2, 22]:
        friday_str += "nd"
    elif friday.day in [3, 23]:
        friday_str += "rd"
    else:
        friday_str += "th"

    # Add the year to the date string
    friday_str += " " + str(friday.year)

    return friday_str


passwordSecret = secrets.password

logging.basicConfig(filename='testing.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
load_time_recorded = 2
for i in secrets.username:
    user = i[0]
    userType = i[1]
    item = i[2]
    time.sleep(5)
    load_time_testing(user, userType, passwordSecret, item)
    #updateCSV(user, userType, load_time_recorded)
    