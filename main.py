import os
import requests
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

base_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

CHROMEDRIVER_PATH = os.path.join(base_dir, "drivers", "chromedriver")


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--remote-debugging-address=0.0.0.0')


@app.post("/seek")
async def login_seek(email: str, password: str):
    "Testing Login In seek.com.au"
    browser = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, options=options)

    # try:
    # Initialize the web driver

    browser.get("https://www.seek.com.au/oauth/login?returnUrl=%2F")

    # Fill in the login form with the appropriate credentials

    wait = WebDriverWait(browser, 10)

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


@app.post("/indeed")
async def login_indeed(email: str, password: str):
    "Testing Login In seek.com.au"
    browser = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH)

    # try:
    # Initialize the web driver

    browser.get("https://secure.indeed.com/auth")

    # Fill in the login form with the appropriate credentials

    wait = WebDriverWait(browser, 10)

    try:
        email_field = wait.until(
            EC.visibility_of_element_located((By.NAME, '__email')))

        email_field.send_keys(email)
        email_field.send_keys(Keys.ENTER)
        # password_field.send_keys(password)

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