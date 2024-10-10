import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.utils import get_page_content, write_file, use_selenium
from dotenv import load_dotenv
load_dotenv()

def main():
    driver = use_selenium()
    start_url = os.getenv('591_FILTER_URL')
    soup = get_page_content(driver, start_url)
    write_file(soup.prettify(), '591.html')

main()