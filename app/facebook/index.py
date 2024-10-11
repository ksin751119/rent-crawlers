import sys
import os
import time
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from libs.utils import get_page_content, write_file, use_selenium
from selenium.webdriver.common.by import By
from helpers.use_login_facebook import use_login_facebook
load_dotenv()
driver = use_selenium()
get_page_content(driver, 'https://www.facebook.com/')
use_login_facebook(driver)
soup = get_page_content(driver, 'https://www.facebook.com/groups/2391145197642950')
#feeds = soup.select('div[role="feed"]')
first_post_index = 1
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
feeds = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"]')
# TODO: get all posts