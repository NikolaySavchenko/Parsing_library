from utils import download_txt
from utils import check_for_redirect
from utils import get_book_details
from utils import download_cover
import argparse


def main():
    parser = argparse.ArgumentParser('Input start ID, end ID')
    parser.add_argument('start_id', nargs='?', type=int, default=1)
    parser.add_argument('end_id', nargs='?', type=int, default=1)
    book_id = parser.parse_args()
    for book_id in range(book_id.start_id, book_id.end_id + 1):
        url_temp = f'https://tululu.org/txt.php?id={book_id}'
        if check_for_redirect(url_temp):
            book_detail = get_book_details(book_id)
            print(book_detail[1], book_detail[4], sep='\n')
            download_txt(url_temp, book_detail[1])
            download_cover(book_detail[2])


if __name__ == '__main__':
    main()
