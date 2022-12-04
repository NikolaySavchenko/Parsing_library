from utils import download_txt
from utils import check_for_redirect
from utils import get_book_details
from utils import download_cover
import argparse


def main(start_id, end_id):
    url = 'https://tululu.org/txt.php?id=32168'
    url_tululu = 'https://tululu.org/txt.php?id=239'
    for id in range(start_id, end_id+1):
        url_temp = f'https://tululu.org/txt.php?id={id}'
        if check_for_redirect(url_temp):
            book_detail = get_book_details(id)
            print(book_detail[1], book_detail[4], sep='\n')
            # print(download_txt(url_temp, book_detail[1]))
            # print(download_cover(id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Input start ID, stop ID')
    parser.add_argument('start_id', nargs='?', default=1)
    parser.add_argument('end_id', nargs='?', default=1)
    start_id = int(parser.parse_args().start_id)
    end_id = int(parser.parse_args().end_id)
    main(start_id, end_id)
