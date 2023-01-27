import os
import time
import requests
from fastapi import FastAPI, HTTPException
from selenium import webdriver
import webdrivermanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess

result = subprocess.run(["which", "chromium"], stdout=subprocess.PIPE)
chromium_path = result.stdout.decode().strip()

base_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

webdrivermanager.chrome.ChromeDriverManager().get_compatible_version()
# CHROMEDRIVER_PATH = os.path.join(base_dir, "drivers", "chromedriver")
CHROME_PATH = chromium_path

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.set_capability("browserVersion", "98")
options.binary_location = CHROME_PATH


@app.get("/")
def start():
    return {"status": True}


@app.get("/seek")
async def login_seek(email: str, password: str):
    "Testing Login In seek.com.au"
    browser = webdriver.Chrome(executable_path=CHROME_PATH, options=options)

    # try:
    # Initialize the web driver

    browser.get("https://www.seek.com.au/oauth/login?returnUrl=%2F")

    # Fill in the login form with the appropriate credentials

    wait = WebDriverWait(browser, 5)

    email_field = wait.until(
        EC.visibility_of_element_located((By.ID, 'emailAddress')))
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, 'password')))

    email_field.send_keys(email)
    password_field.send_keys(password)

    submit_button = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[type="submit"]')))
    submit_button.click()

    try:
        # Wait for the login to complete
        wait.until(EC.url_changes(browser.current_url))
        print('DONE')
        browser.close()
        return {"status": True, "message": "Seek logged in successfully"}

    except Exception as e:
        print(e)
        browser.close()
        return {"status": False, "message": "Seek login failed"}


@app.get("/indeed")
async def login_indeed(email: str, password: str):
    "Testing Login In seek.com.au"
    browser = webdriver.Chrome(executable_path=CHROME_PATH, options=options)

    # try:
    # Initialize the web driver

    browser.get("https://secure.indeed.com/auth")

    # Fill in the login form with the appropriate credentials

    wait = WebDriverWait(browser, 7)

    email_field = wait.until(
        EC.visibility_of_element_located((By.NAME, '__email')))

    for character in email:
        email_field.send_keys(character)
        time.sleep(0.5)  # delay for 0.1 seconds
    # email_field.send_keys(email)
    email_field.send_keys(Keys.ENTER)
    # password_field.send_keys(password)
    try:

        login_with_pass = wait.until(EC.visibility_of_element_located(
            (By.ID, 'auth-page-google-password-fallback')))
        login_with_pass.click()

        pass_field = wait.until(
            EC.visibility_of_element_located((By.NAME, '__password')))
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.ENTER)

        # Wait for the login to complete
        wait.until(
            EC.visibility_of_element_located((By.NAME, 'passcode')))
        browser.close()
        return {"status": True, "message": "Indeed logged in successfully"}

    except Exception as e:
        print(e)
        browser.close()
        return {"status": False, "message": "Indeed login failed"}
