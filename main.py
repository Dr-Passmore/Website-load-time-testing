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
    
    if 'demo' in secrets.target_url:
        environment = "UAT"
    else:
        environment = "Live"
    
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
    if userType == "Admin" or userType == "StoreAssistant":
        wait.until(EC.visibility_of_element_located((By.ID, "form_panel_icons")))
       
    else:     
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dashboard-outer-wrapper")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded,environment)
    logging.info("logged into system")
    time.sleep(longDelay())
    if userType == "Student":
        bookItems(driver, wait, user, userType, item, passwordSecret, environment)
    elif userType == "StoreAssistant":
        #bookingLookUp(driver, wait, user, userType, environment)
        storeAssistantProcess(driver, wait, user, userType, item, environment)
        print("Store Assistant")
    else:
        print("admin")
        driver.quit()
        
def bookItems(driver, wait, user, userType, item, passwordSecret, environment):
    '''
    Books items as a student. Each student will book a preselected item found in the Secrets file.
    
    The following variables are passed from the load_time_testing function:
    - driver
    - wait
    - user
    - userType
    - item
    - passwordSecret
    - environment
    '''
    
    try:
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
        updateCSV(user, userType, process, load_time_recorded, environment)
        logging.info("Search completed")
        
        time.sleep(shortDelay())
    
        
        #Timing until item becomes bookable
        process = f"{item} look up time"
        start = timer()
        book_item = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Add to Basket']")))
        book_item.click()
        end = timer()
        load_time_recorded = round(end-start, 2)
        updateCSV(user, userType, process, load_time_recorded, environment)
        logging.info(f"{item} selected for booking")
    
        time.sleep(longDelay())
    except:
        logging.error("Failed in process to find item")
        driver.quit()
        load_time_testing(user, userType, passwordSecret, item)
        
    try:    
        #Moving to the basket
        basket = driver.find_element(By.CSS_SELECTOR, "[aria-label='Basket']")
        process = "Basket load time"
        start = timer()
        basket.click()
        select_start_date = wait.until(EC.visibility_of_element_located((By.ID, "dtp_collection_log")))
        end = timer()
        load_time_recorded = round(end-start, 2)
        updateCSV(user, userType, process, load_time_recorded, environment)
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
        #select_time.select_by_value("11:00:00")
        select_time.select_by_value("09:30:00")
        
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
        #select_time.select_by_value("11:45:00")
        select_time.select_by_value("10:30:00")
        
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
        updateCSV(user, userType, process, load_time_recorded, environment)
        logging.info(f"Return date and Time Selected after {load_time_recorded}")
        
        time.sleep(shortDelay())
        
        
        process = "Avalibility Check"
        start = timer()
        check_avalibility.click()
        booking = wait.until(EC.visibility_of_element_located((By.ID, "basket-review-content"))) 
        end = timer()
        load_time_recorded = round(end-start, 2)
        updateCSV(user, userType, process, load_time_recorded, environment)
        logging.info("Avalibility check completed")
        
        time.sleep(longDelay())
        
        basket_booking = booking.find_element(By.CSS_SELECTOR, "[aria-label='Book']")
        
        process = "Booking button pressed"
        start = timer()
        basket_booking.click()
        
        
        #terms_toggle = driver.find_element(By.CSS_SELECTOR, "label[for='basket_terms']")
        terms_toggle = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='basket_terms']")))
        end = timer()
        load_time_recorded = round(end-start, 2)
        updateCSV(user, userType, process, load_time_recorded, environment)
        logging.info("Booking form loaded")
        terms_toggle.click()
        
        time.sleep(shortDelay())
        
        
        booking_form = driver.find_element(By.ID, "basket-form-content")
        booking_note = booking_form.find_element(By.XPATH, '//*[@id="basket_notes"]')
        booking_note.click()
        testingNote = f"performance testing - item booked '{item}' on {datetime.now().date()} by Dr Passmore"
        for i in testingNote:
            booking_note.send_keys(i)
            time.sleep(0.1)
        book = booking_form.find_element(By.CSS_SELECTOR, "[aria-label='Book']")
        book.click()
        
        time.sleep(longDelay())
        
        #updateCSV(user, userType, load_time_recorded)
        
        print("order completed")
        
        deleteBooking(driver, wait, user, userType, environment)
        
    except:
        logging.error("Failed to book item")
        cleanupPartlyCompleted(driver, wait, user, userType, item, environment)
        
def deleteBooking (driver, wait, user, userType, environment):
    '''
    Clears booking once created
    '''
    time.sleep(longDelay())
    dashboard = driver.find_element(By.XPATH, '//*[@id="side-nav"]/span[2]/a/span/span[1]')
    
    start = timer()
    process = "Return to Dashboard"
    dashboard.click()     
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dashboard-outer-wrapper")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded,environment)
    logging.info("Returned to dashboard")
    
    my_booking = driver.find_element(By.LINK_TEXT, "My Bookings")
    process = "Load My Bookings Page"
    start = timer()
    my_booking.click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "booking-group-card")))
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded,environment)
    logging.info("My bookings page loaded")
    
    time.sleep(longDelay())
        
    cancel_all = driver.find_element(By.CSS_SELECTOR, "[aria-label='Cancel All']")
    time.sleep(shortDelay())
    cancel_all.click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "cancel-booking-content")))
    time.sleep(shortDelay())
    cancelReason = driver.find_element(By.ID, "cancel-notes")
    cancelReason.click()
    testingNote = f"performance testing - item '{item}' cancelled on {datetime.now().date()} by Dr Passmore"
    for i in testingNote:
            cancelReason.send_keys(i)
            time.sleep(0.1)
    cancelForm = driver.find_element(By.ID, "cancel-booking-content")
    completeCancel = cancelForm.find_element(By.CSS_SELECTOR, "[aria-label='Cancel Booking']")
    completeCancel.click()
    
    time.sleep(15)
    driver.quit()

def storeAssistantProcess(driver, wait, user, userType, item, environment):
    
    logging.info("Store assistant process started")
    
    storeDeskBooking(driver, wait, user, userType, item, environment)
    
    assetManagementPage(driver, wait, user, userType, environment)
    
    time.sleep(shortDelay())
    
    charges_table(driver, wait, user, userType, environment)
    
    time.sleep(shortDelay())

    paymentsPage(driver, wait, user, userType, environment)

    time.sleep(shortDelay())
    
    manageUsers(driver, wait, user, userType, environment)
    
    time.sleep(shortDelay())
    
    bookingManagement(driver, wait, user, userType, environment)
    
    time.sleep(shortDelay())
    
    storeDeskBooking(driver, wait, user, userType, item, environment)
    
    time.sleep(longDelay())
    driver.quit()
    logging.info("Store assistant process completed")
    
    
    
def assetManagementPage(driver, wait, user, userType, environment):
    '''
    Loads the Asset management page. Waits until the table has loaded and records load time.
    '''
    logging.info("Asset Management Page selection")
    page_menu = driver.find_element(By.ID, "page-menu")
    
    page_menu.click()

    time.sleep(shortDelay())

    booking_management = driver.find_element(By.CSS_SELECTOR, "[aria-label='Assets']")
    booking_management.click()
    
    time.sleep(shortDelay())
    
    booking_management = driver.find_element(By.XPATH, '//*[@id="docMainMenuSub"]/div[2]/a')
    
    process = "Load Asset Management Table"
    start = timer()
    
    booking_management.click()
    
    
    wait.until(EC.visibility_of_element_located((By.ID, "stockGrid_body")))
    
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded, environment)
    logging.info(f"Asset Manager Table Loaded after {load_time_recorded} seconds")
     
def charges_table(driver, wait, user, userType, environment):
    '''
    Loads the Charges page. Waits until the table has loaded and records load time.
    '''
    logging.info("Charges Table Page selection")
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()
    
    Tariffs = driver.find_element(By.CSS_SELECTOR, "[aria-label='Tariffs and Fines']")
    Tariffs.click()
    
    time.sleep(shortDelay())
    
    Tariffs = driver.find_element(By.XPATH, '//*[@id="docMainMenuSub"]/div[3]/a')
    
    process = "Load Charges Table"
    start = timer()
    
    Tariffs.click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "chargesGrid_frame")))
    
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded, environment)
    logging.info(f"Charges Table Loaded after {load_time_recorded} seconds")
    
def paymentsPage(driver, wait, user, userType, environment):
    '''
    Loads the Payments page. Waits until the table has loaded and records load time.
    '''
    logging.info("Payment Table Page selection")
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()
    
    Tariffs = driver.find_element(By.CSS_SELECTOR, "[aria-label='Tariffs and Fines']")
    Tariffs.click()
    
    time.sleep(shortDelay())
    
    Tariffs = driver.find_element(By.XPATH, '//*[@id="docMainMenuSub"]/div[4]/a')
    
    process = "Load Payment Table"
    start = timer()
    
    Tariffs.click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "paymentsGrid_body")))
    
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded, environment)
    logging.info(f"Payment Table Loaded after {load_time_recorded} seconds")
    
def manageUsers(driver, wait, user, userType, environment):
    '''
    Loads the Manage Users page. Waits until the table has loaded and records load time.
    '''
    
    logging.info("Manage Users Page Selection")
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()
    
    Tariffs = driver.find_element(By.CSS_SELECTOR, "[aria-label='Users']")
    Tariffs.click()
    
    time.sleep(shortDelay())
    
    Tariffs = driver.find_element(By.XPATH, '//*[@id="docMainMenuSub"]/div[2]/a')
    
    process = "Load Manage Users Table"
    start = timer()
    
    Tariffs.click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "usersGrid_body")))
    
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded, environment)
    logging.info(f"Manage Users Table Loaded after {load_time_recorded} seconds")

def bookingManagement(driver, wait, user, userType, environment):
    '''
    Loads the Booking management page. Waits until the table has loaded and records load time.
    '''
    
    try:
        logging.info("Booking Management Page Selection")
        page_menu = driver.find_element(By.ID, "page-menu")
        page_menu.click()
        
        Tariffs = driver.find_element(By.CSS_SELECTOR, "[aria-label='Booking Management']")
        Tariffs.click()
        
        time.sleep(shortDelay())
        
        Tariffs = driver.find_element(By.XPATH, '//*[@id="docMainMenuSub"]/div[2]/a')
    except:
        logging.error("Failed to Navigate to Booking Management Page Selection")
    try:
        process = "Load Booking Management Table"
        start = timer()
        
        Tariffs.click()
        
        wait.until(EC.visibility_of_element_located((By.ID, "managebookingsGrid_body")))
        
        end = timer()
        load_time_recorded = round(end-start, 2)
        updateCSV(user, userType, process, load_time_recorded, environment)
    except:
        logging.error(f"Timeout - Over 5 minutes")
        load_time_recorded = 300
    logging.info(f"Booking Management Table Loaded after {load_time_recorded} seconds")
    
def storeDeskBooking(driver, wait, user, userType, item, environment):
    
    #account to book and return item from
    student = secrets.storeBooking[user]
    
    logging.info("Store Desk Process Started")
    
    page_menu = driver.find_element(By.ID, "page-menu")
    page_menu.click()
    
    bookingManagement = driver.find_element(By.CSS_SELECTOR, "[aria-label='Booking Management']")
    bookingManagement.click()
        
    store_desk = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Store Desk")))
    store_desk.click()
    
    time.sleep(shortDelay())
    
    collectpage = driver.find_element(By.XPATH, '//*[@id="sd-container-menu"]/ul/li[3]')
    
    collectpage.click()
    
    time.sleep(shortDelay())
    
    bookto = driver.find_element(By.XPATH, '//*[@id="bookedto_search"]')
    bookto.click()
    for i in student:
        bookto.send_keys(i)
        time.sleep(0.1)
    bookto.send_keys(Keys.ENTER)
    
    time.sleep(shortDelay())
    
    itemBooking = driver.find_element(By.XPATH, '//*[@id="collect_asset_search"]')
    itemBooking.click()
    for i in item:
        itemBooking.send_keys(i)
        time.sleep(0.1)
    itemBooking.send_keys(Keys.ENTER)
    
    time.sleep(longDelay())
    
    itemlist = driver.find_element(By.CLASS_NAME, 'ua-search-list-item')
    itemlist.click()
    
    
    
    
    start = timer()
    process = "Find item for adhoc booking"
    returnTimeItem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Return Date']")))
    
    end = timer()
    load_time_recorded = round(end-start, 2)
    updateCSV(user, userType, process, load_time_recorded, environment)
    time.sleep(shortDelay())
    #returnTimeItem.click()
    
    
  
    
    itemBooking.send_keys(Keys.PAGE_DOWN)
    
    time.sleep(shortDelay())
    
    bookingNotes = driver.find_element(By.XPATH, '//*[@id="collect_notes"]')
    testingNote = f"performance testing - item booked '{item}' on {datetime.now().date()} by Dr Passmore"
    bookingNotes.click()
    for i in testingNote:
        bookingNotes.send_keys(i)
        time.sleep(0.1)
    
    time.sleep(shortDelay())
    
    process = driver.find_element(By.XPATH, '//*[@id="sd-container-content"]/div[5]/div/div[8]/div/div/div/div/div/button')
    process.click()
    
    
    time.sleep(longDelay())
    
    
    
    

#! new approach
def bookingLookUp(driver, wait, user, userType, environment):
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
    

    
    
    
    
def cleanupPartlyCompleted(driver, wait, user, userType, item, environment):
    '''
    The cleanupPartlyCompleted function exists to deal with failures to complete bookings. 
    
    If the item is in a basket then the search process will show the item but with an "Update icon" rather than book. 
    
    This process removes the failed item from basket and then restarts the process. 
    
    Varibles passed to cleanupPartlyCompleted by bookItems function includes:
    - driver
    - wait
    - user
    - userType
    - item
    - environment
    '''
    #! Required for failures going to basket or failure to complete order
    
    
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
    updateCSV(user, userType, process, load_time_recorded, environment)
    logging.info("Search completed")
    
    time.sleep(shortDelay())
    
    remove_item = driver.find_element(By.CSS_SELECTOR, "[aria-label='Minus asset quantity']")
    remove_item.click()
    
    time.sleep(shortDelay())
    
    update_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Update']")
    update_button.click()
    
    time.sleep(shortDelay())
    
    driver.quit()
    
    load_time_testing(user, userType, passwordSecret, item)

def updateCSV(user, userType, process, load_time_recorded, environment):
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
               environment,
               process,
               load_time_recorded]
    
    with open("LoadingTimeResults.csv", "a", newline='') as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(new_row)
    csvFile.close()
    logging.info(f"CSV updated with {new_row}")
    
def longDelay():
    '''
    Provides a random delay between 5 and 10 seconds
    '''
    return randint(5,10)

def shortDelay():
    '''
    Provides a random delay between 2 and 4 seconds
    '''
    return randint(2, 4)

def dateSelection():
    '''
    Gets date in the future to minimise impact on students. In particular a week on Friday
    '''
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
loops = 5


for i in range(loops):
    for i in secrets.username:
        user = i[0]
        userType = i[1]
        item = i[2]
        load_time_testing(user, userType, passwordSecret, item)
       
    