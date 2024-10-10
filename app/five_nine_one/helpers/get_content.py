import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from libs.utils import get_page_content, use_selenium
from dotenv import load_dotenv
load_dotenv()
def get_content():
    driver = use_selenium()
    start_url = os.getenv('591_FILTER_URL')
    soup = get_page_content(driver, start_url)
    return soup.prettify()