from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://rent.591.com.tw/list?keywords=%E5%8F%A4%E4%BA%AD&price=10000_20000')
print(driver.title)
soup = BeautifulSoup(driver.page_source, 'html.parser')
fp = open('temp/591rent.html', 'w', encoding='utf-8')
fp.write(soup.prettify())
fp.close()
driver.quit()