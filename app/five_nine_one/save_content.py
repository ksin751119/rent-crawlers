import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.utils import write_file
from helpers.get_content import get_content

def main():
    write_file(get_content(), '591.html')

main()