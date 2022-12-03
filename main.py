from utils import download_txt
from utils import check_for_redirect
from utils import get_book_details
from utils import download_cover


def main():
    url = 'https://tululu.org/txt.php?id=32168'
    url_tululu = 'https://tululu.org/txt.php?id=239'
    for id in range(1, 11):
        url_temp = f'https://tululu.org/txt.php?id={id}'
        if check_for_redirect(url_temp):
            book_detail = get_book_details(id)
            print(download_txt(url_temp, book_detail[1]))
            print(download_cover(id))


if __name__ == '__main__':
    main()
