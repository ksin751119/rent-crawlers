import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()
SESSION_ID = os.getenv('591_PHPSESSID')
url = 'https://rent.591.com.tw/list?keywords=%E5%8F%A4%E4%BA%AD&price=10000_20000'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'cookie': 'webp=1; PHPSESSID=' + SESSION_ID + '; urlJumpIp=1; T591_TOKEN=' + SESSION_ID + '; is_new_index=1; is_new_index_redirect=1; _gcl_au=1.1.1440598302.1728096357; _gid=GA1.3.1788163377.1728096357; _clck=l5a6ga%7C2%7Cfpr%7C0%7C1739; timeDifference=0; tw591__privacy_agree=1; __lt__cid=7e5eaf1a-e4d6-408c-81c9-6aed0f143fb2; __lt__sid=0c02f881-4aabcd14; _fbp=fb.2.1728096663618.505309817728194896; __one_id__=01J9D9CYC9EZ8PSVFZ1FN6YR9S; last_search_type=2; 591_new_session=eyJpdiI6Ijh0aDlHbHU5UWhYcGdiN0RUeUpxQUE9PSIsInZhbHVlIjoiVjBYVUpmYUtPbmxWaGlHNDIxQmFEK0hYVDlSaGJyYnMxaXhGSkNZS3NxbzQ5MVZVamI2VnhBL2s1L3pvbWpONDBiY1hWQmZ5TjNtZ3lyMUVmQXo5QUU0UHpRS0x3SCtlRGtMS2pNaG1pakQ0SXhYTlV4KzBMWklVeVBKekZ0cnAiLCJtYWMiOiJhZGU1YWJlMjU5YzYzYWU3MzA2NTVjMGRkMmIxY2M0NWRkOWI4ZWMxYjkzMmE4NTgwNjliZTNkMjA4YTlkMzZkIiwidGFnIjoiIn0%3D; sale_search_trace_cache=%7B%22actionType%22%3A3%2C%22keyword%22%3A%22%E5%8F%A4%E4%BA%AD%22%2C%22uniqueTipWord%22%3A%22%22%7D; _gat=1; _ga_H07366Z19P=GS1.3.1728096357.1.1.1728097642.60.0.0; _ga=GA1.1.1549737761.1728096357; _clsk=1akmezo%7C1728097644129%7C69%7C0%7Cp.clarity.ms%2Fcollect; _ga_HDSPSZ773Q=GS1.1.1728096357.1.1.1728097657.18.0.0'
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.select('div.content')
    for content in contents:
        link = content.select_one('a.title')
        if (link != None):
          print(link['href'])
          print(link.text)