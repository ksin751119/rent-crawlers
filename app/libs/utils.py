from bs4 import BeautifulSoup
from selenium import webdriver
def get_page_content(driver, url):
    driver.get(url)
    print('getting page content of title: ', driver.title)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def write_file(output, file_name):
    with open(f'temp/{file_name}', 'w') as f:
        f.write(output)
        return True

def use_selenium():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver
