import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from libs.utils import get_page_content, use_selenium
from dotenv import load_dotenv
load_dotenv()
def get_content():
    driver = use_selenium()
    start_url = os.getenv('591_FILTER_URL')
    if (start_url is None):
        print('Please set 591_FILTER_URL in .env')
        print('If .env is not exist, please create one at the root directory')
        print('Example: 591_FILTER_URL=https://rent.591.com.tw/list?keywords=古亭&price=10000_20000')
        sys.exit()
    soup = get_page_content(driver, start_url)
    return soup.prettify()