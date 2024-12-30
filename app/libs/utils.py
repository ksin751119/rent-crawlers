from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def use_disable_chrome_annoyings():
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
    return options

def get_page_content(driver, url):
    driver.get(url)
    print('Getting page content of title: ', driver.title)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def write_file(output, file_name):
    with open(f'static/{file_name}', 'w') as f:
        f.write(output)
        return True

def use_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 無頭模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)
