import sys
import os
import time
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from libs.utils import get_page_content, write_file, use_selenium
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
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

def get_google_sheets_service():
    """建立 Google Sheets API 服務連線"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_KEY_FILE'),  # 請替換成您的憑證檔案路徑
        scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=creds)

def read_sheet_data(service):
    """讀取 Google Sheet 資料"""
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')  # 請替換成您的試算表 ID
    RANGE_NAME = '591Rent!A:G'  # 調整範圍

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    return result.get('values', [])

def update_sheet_data(service, new_data):
    """更新 Google Sheet 資料"""
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    RANGE_NAME = '591Rent!A:G'  # 調整範圍

    body = {
        'values': new_data
    }
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

def send_line_notification(message):
    """發送 Line 通知"""
    LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    print("data", data)
    requests.post(url, headers=headers, data=data)

def extract_house_id(url):
    """從 URL 中提取房屋 ID"""
    # print("url", url)
    return url.split('/')[-1]

def write_recommends(soup):
    columns = ['title', 'price', 'address', 'area', 'link']
    data = []
    recommendWares = soup.select('div.recommend-ware')
    for content in recommendWares:
        house = {
            "title": content.select_one('a.title').text,
            "price": content.select_one('div.price-info').text,
            "address": content.select_one('span.address').text,
            "area": content.select_one('span.area').text,
            "link": content.select_one('a.title')['href'].replace('\/', '/')
        }
        data.append(house)
    df = pd.DataFrame(data, columns=columns)
    json_output = df.to_json(orient='records')
    write_file(json_output, '591recommend.json')
    return data


def write_normal(driver, soup, start_url):
    columns = ['title', 'price', 'address', 'floor', 'area', 'images', 'link']
    data = []
    page = 1

    while soup.select_one('.empty') is None:
        print(f'getting page {page}')
        items = soup.select('.list-wrapper .item')

        for item in items:
            image_lst = [img['data-src'] for img in item.select('img[alt="物件圖片"]')]

            house = {
                "title": item.select_one('a.link').text,
                "price": generate_price_text(item.select_one('div.item-info-price')),
                "address": generate_address_text(item.select('.item-info-txt')[1]),
                "floor": generate_floor_text(item.select('span.line')[1]),
                "area": generate_area_text(item.select('span.line')[0]),
                # "images": image_lst,
                "link": item.select_one('a.link')['href']
            }
            data.append(house)

        print(f'successfully crawl page: {page}')
        page += 1
        soup = get_page_content(driver, start_url + f'&page={page}')
        time.sleep(1)

    df = pd.DataFrame(data, columns=columns)
    json_output = df.to_json(orient='records')
    write_file(json_output, '591normal.json')



    return data

def main():
    driver = use_selenium()
    start_url = os.getenv('591_FILTER_URL')
    if (start_url is None):
        print('Please set 591_FILTER_URL in .env')
        print('If .env is not exist, please create one at the root directory')
        print('Example: 591_FILTER_URL=https://rent.591.com.tw/list?keywords=古亭&price=10000_20000')
        sys.exit()
    soup = get_page_content(driver, start_url)
    time.sleep(1)
    # rental_houses =write_recommends(soup)
    rental_houses =write_normal(driver, soup, start_url)


    # # 取得 Google Sheets 服務
    sheets_service = get_google_sheets_service()

    # # 讀取現有的 Sheet 資料
    existing_data = read_sheet_data(sheets_service)
    # print("existing_data", existing_data)
    existing_ids = set(extract_house_id(row[4]) for row in existing_data[1:] if len(row) > 4)  # E 欄位是 link
    # print("existing_ids", existing_ids)



    # print("existing_ids", existing_ids)
    # 過濾新的物件
    new_items = []
    for row in rental_houses:
        # print ("row", row)
        house_id = extract_house_id(row["link"])
        # print("house_id", house_id)
        if house_id not in existing_ids:
            new_items.append([
                row["title"],
                row["price"],
                row["address"],
                row["area"],
                row["link"]
            ])

            message = f"\n找到新物件！\n標題：{row['title']}\n連結：{row['link']}"
            send_line_notification(message)

    print("new_items", len(new_items))
    if new_items:
        update_sheet_data(sheets_service, new_items)


main()
