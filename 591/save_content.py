from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
import os
load_dotenv()

def get_page_content(driver, url):
    driver.get(url)
    print('getting page content of title: ', driver.title)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def write_html(html_output, file_name):
    with open(f'temp/{file_name}', 'w') as f:
        f.write(html_output)

def main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    start_url = os.getenv('591_FILTER_URL')
    soup = get_page_content(driver, start_url)
    write_html(soup.prettify(), '591.html')

main()