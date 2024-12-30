from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 使用 ChromeDriver Manager 自動管理 driver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Chrome 瀏覽器初始化失敗: {str(e)}")
        raise
