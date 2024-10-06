import pandas as pd
import os
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
load_dotenv()

def render_images(image_list):
    return ''.join([f'<img src="{img}" width="100" />' for img in image_list])
def render_link(link, title):
    return f'<a href="{link}" target="_blank">{title}</a>'
def get_page_content(driver, url):
    driver.get(url)
    print('getting page content of title: ', driver.title)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup
def write_html(html_output, file_name):
    with open(f'temp/{file_name}', 'w') as f:
        f.write(html_output)
def write_recommends(soup):
    columns = ['title', 'price', 'address', 'area', 'images', 'link']
    data = []
    recommendWares = soup.select('div.recommend-ware')
    for content in recommendWares:
        title = content.select_one('a.title').text
        price = content.select_one('div.price-info').text
        address = content.select_one('span.address').text
        area = content.select_one('span.area').text
        image_lst = []
        images = content.select('img[alt="物件圖片"]')
        for image in images:
            image_lst.append(image['data-src'])
        link = content.select_one('a.title')['href']
        data.append([title, price, address, area, image_lst, link])
    df = pd.DataFrame(data, columns=columns)
    df['images'] = df['images'].apply(render_images)
    df['link'] = df.apply(lambda x: render_link(x['link'], x['title']), axis=1)
    html_output = df.to_html(escape=False)
    write_html(html_output, '591recommend.html')
def write_normal(soup):
    columns = ['title', 'price', 'address', 'floor', 'area', 'images', 'link']
    data = []
    items = soup.select('.list-wrapper .item')
    for item in items:
        image_lst = []
        images = item.select('img[alt="物件圖片"]')
        for image in images:
            image_lst.append(image['data-src'])
        title = item.select_one('a.link').text
        link = item.select_one('a.link')['href']
        area_and_floor = item.select('span.line')
        area = next((span for span in area_and_floor if "坪" in span.get_text()), None).get_text()
        floor = next((span for span in area_and_floor if "F" in span.get_text()), None).get_text()
        address = item.select_one('div.item-info-txt').text
        price = item.select_one('div.item-info-price').text
        data.append([title, price, address, floor, area, image_lst, link])
    df = pd.DataFrame(data, columns=columns)
    df['images'] = df['images'].apply(render_images)
    df['link'] = df.apply(lambda x: render_link(x['link'], x['title']), axis=1)
    html_output = df.to_html(escape=False)
    write_html(html_output, '591normal.html')
def main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    start_url = os.getenv('591_FILTER_URL')
    soup = get_page_content(driver, start_url)
    write_recommends(soup)
    write_normal(soup)

main()