import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.command import Command
import http.client
import socket
import json


def run():
    chromeOptions = Options()
    # chromeOptions.add_experimental_option('w3c', False)
    global driver
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chromeOptions)
    driver.implicitly_wait(3)
    driver.get('https://google.com/')
    writeSession(driver)
    f = open("allCookies.txt", "r")
    cookies = f.readlines()

    for cookie in cookies:
        # * string --> dict
        dicCookie = json.loads(cookie)
        # * if cookies.name != "__Host-user_session_same_site" don't add cookie
        if (dict.get(dicCookie, "name") not in ["__Host-user_session_same_site", "...other broken cookie names"]):
            driver.add_cookie(dicCookie)
        # * use this to see what cookies are not being added
        #! else: print(dicCookie)

    print("Braden has baked the cookies, your welcome AJ <3")
    print('Finished Initiating Chrome Driver')


def writeSession(driver):
    url = driver.command_executor._url
    session_id = driver.session_id
    f = open("sessioninfo.txt", "w")
    f.write(f"{url}\n")
    f.write(f"{session_id}")
    f.close()
    print('Wrote webdriver session details')


class Scraper():
    # ? on close tab or window can you save cookies? (beforeUnload/beforeUnMount)
    def __init__(self):
        self.driver = attachToSession()

    def getGithub(self):
        #! run get cookies to save previous pages cookies
        try:
            driver = self.driver
            driver.get('https://www.github.com/')
            time.sleep(2)
            print('Sleep done..')
            return 200
        except Exception as e:
            print(e)
            raise e

    def getStackOverflow(self):
        #! run get cookies to save previous pages cookies
        try:
            driver = self.driver
            driver.get('https://stackoverflow.com')
            time.sleep(2)
            print('Sleep done..')
            return 200
        except Exception as e:
            print(e)
            raise e

    def saveCookies(self):
        try:
            driver = self.driver
            # TODO save cookies and update existing cookies (tip go off cookie name (subtip: if any data in cookie is different, update that cookie))
            #! read cookies file and update/add new cookies to variable, continue w/ dumping new varable into cookie file
            #! check exp dates on existing cookies (remove old cookies if not updated)
            # don't use this, use the new variable with updated cookies
            cookies = driver.get_cookies()
            f = open("allCookies.txt", "w")
            for cookie in cookies:
                f.write(json.dumps(cookie) + "\n")
            f.close()
            print('Saved Cookies')
            return 200
        except Exception as e:
            print(e)
            raise e


def attachToSession():
    # Code Reference : https://stackoverflow.com/a/48194907/11217153
    # The stackover flow answer was adapted.
    f = open("sessioninfo.txt", "r")
    lines = f.readlines()
    url = lines[0]
    session_id = lines[1]
    session_id.strip()
    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver
