import requests
import re
from bs4 import BeautifulSoup
from utils import check_for_redirect


def get_id(page):
    url = f'https://tululu.org/l55/{page}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find_all(class_='d_book')
    book_hrefs = [book.find('a')['href'] for book in books]
    book_ids = [int(re.sub('/|b', '', href)) for href in book_hrefs]
    return book_ids


def main():
    for id in get_id(1):
        print(f'https://tululu.org/b{id}')


if __name__ == '__main__':
    main()
