from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from user_input import InputWindow
import time, os, sys

#Likes activity entries in the given feed
def like_activity_entries():
    for i in range(int(load_more)):
        driver.find_element(By.CLASS_NAME, value="load-more").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    activity_entries = driver.find_elements(By.CLASS_NAME, value="activity-entry")
    likes = []

    for entry in activity_entries:
        activity_username = entry.find_element(By.CLASS_NAME, value="name").text.strip()
        if activity_username != username:
            try:
                likes.append(entry.find_element(By.CSS_SELECTOR, value='.likes .button:not(.liked)'))
            except NoSuchElementException:
                pass

    for like in likes:
        try:
            like.click()
        except ElementClickInterceptedException:
            pass

        try:
            WebDriverWait(driver, 0.2).until(expected_conditions.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Too many likes created recently')]")))
        except TimeoutException:
            pass
        else:
            time.sleep(65)

#Returns the directory of the app
def get_app_directory():
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

#Creates a new window for the user to enter their details
def create_new_window():
    global user_information, username, email, password, load_more
    try:
        with open(path, "r") as file:
            user_information = file.read().splitlines()
            username = user_information[1]
            email = user_information[2]
            password = user_information[3]
            load_more = user_information[0]
    except FileNotFoundError:
        new_window = InputWindow("", "", "", 0)
    except IndexError:
        new_window = InputWindow("", "", "", 0)
    else:
        new_window = InputWindow(username, email, password, load_more)
    finally:
        if new_window.escape:
            driver.quit()
            sys.exit()
        load_more = new_window.load_more
        username = new_window.username
        email = new_window.email
        password = new_window.password
        with open(path, "w") as file:
            file.write(f"{load_more}\n{username}\n{email}\n{password}")

driver = webdriver.Chrome()
driver.get("https://anilist.co/login")
path = os.path.join(get_app_directory(), "user_information.txt")

#reCAPTCHA and login
create_new_window()
login_fail = True
while login_fail:
    driver.find_element(By.CSS_SELECTOR, value='input[placeholder="Email"]').clear()
    driver.find_element(By.CSS_SELECTOR, value='input[placeholder="Email"]').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, value='input[placeholder="Password"]').clear()
    driver.find_element(By.CSS_SELECTOR, value='input[placeholder="Password"]').send_keys(password)
    time.sleep(20)
    driver.find_element(By.CLASS_NAME, value="submit").click()
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, '[role="alert"]')))
    except TimeoutException:
        login_fail = False
    else:
        create_new_window()
time.sleep(5)

#Following list
like_activity_entries()

#Global list
driver.find_element(By.XPATH, value='//*[@id="app"]/div[3]/div/div/div[1]/h2/div/div[2]/div[2]').click()
time.sleep(2)
like_activity_entries()

driver.quit()

