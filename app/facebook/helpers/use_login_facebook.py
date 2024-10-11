import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
load_dotenv()
def use_login_facebook(driver):
  account_input = driver.find_element(By.ID, 'email')
  password_input = driver.find_element(By.ID, 'pass')
  login_button = driver.find_element(By.ID, 'loginbutton')
  account_input.send_keys(os.getenv('FACEBOOK_ACCOUNT'))
  password_input.send_keys(os.getenv('FACEBOOK_PASSWORD'))
  login_button.click()
  time.sleep(10)