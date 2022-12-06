from utils import download_txt
from utils import get_book_details
from utils import download_cover
import argparse


def main():
    parser = argparse.ArgumentParser('Input start ID, end ID')
    parser.add_argument('start_id', nargs='?', type=int, default=1)
    parser.add_argument('end_id', nargs='?', type=int, default=1)
    book_id = parser.parse_args()
    url = 'https://tululu.org/txt.php'
    for book_id in range(book_id.start_id, book_id.end_id + 1):
        payload = {'id': book_id}
        book_detail = get_book_details(book_id)
        if len(book_detail) == 5:
            download_txt(url, payload, book_detail[1])
            download_cover(book_detail[2])
            print(book_detail[1], book_detail[4], sep='\n')
        else:
            print(book_detail)


if __name__ == '__main__':
    main()
