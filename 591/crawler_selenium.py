import pandas as pd
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
load_dotenv()

def generate_area_text(area_element):
    if area_element is None:
        return ""
    items = area_element.select("i")
    return sort_element_by_style_order(items)
def generate_floor_text(floor_element):
    if floor_element is None:
        return ""
    items = floor_element.select("i")
    return sort_element_by_style_order(items)
def generate_price_text(price_element):
    if price_element is None:
        return ""
    items = price_element.select("i")
    return sort_element_by_style_order(items)
def generate_address_text(address_element):
    if address_element is None:
        return ""
    items: list = address_element.select("i")
    items.pop(0)
    return sort_element_by_style_order(items)
def sort_element_by_style_order(elements: list):
    def sort_fn(x: str):
        order_value = x['style'].split(':')[1].split(';')[0]
        return int(order_value)
    sorted_items = sorted(elements, key=sort_fn)
    result = ''.join([item.text for item in sorted_items])
    return result
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
def write_normal(driver, soup, start_url):
    def get_normal_items(soup):
        items = soup.select('.list-wrapper .item')
        for item in items:
            image_lst = []
            images = item.select('img[alt="物件圖片"]')
            for image in images:
                image_lst.append(image['data-src'])
            title = item.select_one('a.link').text
            link = item.select_one('a.link')['href']
            area_and_floor = item.select('span.line')
            area_data = area_and_floor[0]
            floor_data = area_and_floor[1]
            address_data = item.select('.item-info-txt')[1]
            price_data = item.select_one('div.item-info-price')
            area = generate_area_text(area_data)
            floor = generate_floor_text(floor_data)
            address = generate_address_text(address_data)
            price = generate_price_text(price_data)
            data.append([title, price, address, floor, area, image_lst, link])
    data = []
    page = 1
    while soup.select_one('.empty') is None:
        print(f'getting page {page}')
        get_normal_items(soup)
        print(f'successfully crawl page: {page}')
        page += 1
        soup = get_page_content(driver, start_url + f'&page={page}')
        time.sleep(1)
    columns = ['title', 'price', 'address', 'floor', 'area', 'images', 'link']
    df = pd.DataFrame(data, columns=columns)
    df['images'] = df['images'].apply(render_images)
    df['link'] = df.apply(lambda x: render_link(x['link'], x['title']), axis=1)
    html_output = df.to_html(escape=False)
    write_html(html_output, '591normal.html')
    print('write normal done')
def main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    start_url = os.getenv('591_FILTER_URL')
    soup = get_page_content(driver, start_url)
    write_recommends(soup)
    write_normal(driver, soup, start_url)

main()