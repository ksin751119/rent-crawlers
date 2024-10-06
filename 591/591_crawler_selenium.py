import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
def render_images(image_list):
    return ''.join([f'<img src="{img}" width="100" />' for img in image_list])
def render_link(link, title):
    return f'<a href="{link}" target="_blank">{title}</a>'
columns = ['title', 'price', 'address', 'area', 'images', 'link']
data = []
driver = webdriver.Chrome()
driver.implicitly_wait(10)
url = 'https://rent.591.com.tw/list?keywords=%E5%8F%A4%E4%BA%AD&price=10000_20000'
driver.get(url)
print(driver.title)
soup = BeautifulSoup(driver.page_source, 'html.parser')
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
with open('temp/591recommend.html', 'w') as f:
    f.write(html_output)