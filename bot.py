from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os.path
import sqlite3
import schedule
from datetime import datetime
import os
from db import add_timetable, view_timetable


opt = Options()
# Allowing access to mic, cam, location and notifications
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

# Setting up the path to our webdriver
PATH = os.path.join(os.getcwd() + "/chromedriver")
driver = webdriver.Chrome(PATH, options=opt)

URL = "https://teams.microsoft.com"

# MS TEAMS Credentials
CREDS = {
    'email': os.environ.get('MS_EMAIL'),
    'passwd': os.environ.get('MS_PASSWORD')
}


def login():
    """Function to log in to your MS TEAMS account"""
    global driver  # referring to the global driver
    driver.get(URL)
    WebDriverWait(driver, 10000).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'body')))

    # login required
    print("logging into MS TEAMS")
    emailField = driver.find_element_by_id("i0116")
    emailField.click()
    emailField.send_keys(CREDS['email'])

    # Press the Next button
    driver.find_element_by_id("idSIButton9").click()
    time.sleep(5)

    passwordField = driver.find_element_by_id("i0118")
    passwordField.click()
    passwordField.send_keys(CREDS['passwd'])

    driver.find_element_by_id("idSIButton9").click()  # Sign in button
    time.sleep(5)

    driver.find_element_by_id("idSIButton9").click()  # remember login

    # Changing view to list view from grid view
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "personDropdown"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//button[@class='ts-sym left-align-icon']")))

    driver.find_elements_by_xpath(
        "//button[@class='ts-sym left-align-icon']")[-1].click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='theme-item']")))
    driver.find_element_by_xpath(
        "//li[@aria-label='List layout button']").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='close-container app-icons-fill-hover']"))).click()

    print("Logged in successfully")


def joinmeeting(meeting_name, start_time, end_time):
    global driver

    available_meetings = driver.find_elements_by_class_name(
        "name-channel-type")

    for i in available_meetings:
        if meeting_name.lower() in i.get_attribute('innerHTML').lower():
            print("JOINING MEETING ", meeting_name)
            i.click()
            break

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "ts-calling-join-button"))).click()
    except:
        # join button not found
        # refresh every minute until found
        k = 1
        while(k <= 10):
            print("Join button not found, trying again")
            time.sleep(60)
            driver.refresh()
            joinmeeting(meeting_name, start_time, end_time)

            k += 1
        print("Seems like there is no meeting today.")

    time.sleep(4)
    webcam = driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
    if(webcam.get_attribute('title') == 'Turn camera off'):
        webcam.click()
    time.sleep(1)

    microphone = driver.find_element_by_xpath(
        '//*[@id="preJoinAudioButton"]/div/button/span[1]')
    if(microphone.get_attribute('title') == 'Mute microphone'):
        microphone.click()

    time.sleep(1)
    joinnowbtn = driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
    joinnowbtn.click()

    # now schedule leaving meeting
    tmp = "%H:%M"

    meet_running_time = datetime.strptime(
        end_time, tmp) - datetime.strptime(start_time, tmp)

    time.sleep(meet_running_time.seconds)

    driver.find_element_by_class_name("ts-calling-screen").click()

    driver.find_element_by_xpath(
        '//*[@id="teams-app-bar"]/ul/li[3]').click()  # come back to homepage
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
    print("Meeting left")


def scheduler():
    db = sqlite3.connect('timetable.db')
    mycursor = db.cursor()
    for row in mycursor.execute('SELECT * FROM timetable'):
        # schedule all meeting
        name = row[0]
        start_time = row[1]
        end_time = row[2]
        day = row[3]

        if day.lower() == "monday":
            schedule.every().monday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

        if day.lower() == "tuesday":
            schedule.every().tuesday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

        if day.lower() == "wednesday":
            schedule.every().wednesday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

        if day.lower() == "thursday":
            schedule.every().thursday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

        if day.lower() == "friday":
            schedule.every().friday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

        if day.lower() == "saturday":
            schedule.every().saturday.at(start_time).do(
                joinmeeting, name, start_time, end_time)
            print(f"Scheduled meeting {name} on {day} at {start_time}")

    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    choice = int(
        input(("1. Modify Timetable\n2. View Timetable\n3. Start MS-Teams Bot\nEnter option : ")))

    if(choice == 1):
        add_timetable()
    elif(choice == 2):
        view_timetable()
    elif(choice == 3):
        login()
        scheduler()
    else:
        driver.quit()
        exit()
