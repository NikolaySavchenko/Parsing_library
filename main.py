from utils import download_txt
from utils import get_book_details
from utils import download_cover
from utils import get_title_author
from utils import get_cover
from utils import get_genres

from time import sleep
import argparse
import requests


def main():
    parser = argparse.ArgumentParser('Input start ID, end ID')
    parser.add_argument('start_id', nargs='?', type=int, default=1)
    parser.add_argument('end_id', nargs='?', type=int, default=1)
    book_ids = parser.parse_args()
    url = 'https://tululu.org/txt.php'
    book_id = book_ids.start_id
    while book_id <= book_ids.end_id:
        payload = {'id': book_id}
        try:
            book_detail = get_book_details(book_id)
            book_title = get_title_author(book_detail, book_id)['title']
            download_txt(url, payload, book_title)
            download_cover(get_cover(book_detail))
            print(book_title, *get_genres(book_detail), sep='\n')
            book_id += 1
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка сайта при id {book_id}: {error}')
            book_id += 1
            continue
        except requests.exceptions.ConnectionError as error1:
            print(f'Ошибка сети {error1}')
            sleep(30)
            continue


if __name__ == '__main__':
    main()
