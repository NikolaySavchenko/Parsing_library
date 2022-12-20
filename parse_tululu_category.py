import requests
import re
import json
import argparse
from bs4 import BeautifulSoup
from utils import check_for_redirect
from utils import download_txt
from utils import get_book_details
from utils import download_cover
from utils import get_title
from utils import get_cover
from utils import get_genres
from utils import get_comments
from utils import get_autor


def get_id(page):
    url = f'https://tululu.org/l55/{page}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.select('.d_book a[href^="/b"]')
    book_ids = {int(re.sub('/|b', '', book['href'])) for book in books}
    return list(book_ids)


def main():
    parser = argparse.ArgumentParser('Input start page, end page and other settings')
    parser.add_argument('start_page', nargs='?', type=int, default=1)
    parser.add_argument('end_page', nargs='?', type=int, default=702)
    parser.add_argument('--dest_folder', type=bool, default=False)
    parser.add_argument('--skip_imgs', type=bool, default=False)
    parser.add_argument('--skip_txt', type=bool, default=False)
    parser.add_argument('--json_path', type=bool, default=False)
    settings = parser.parse_args()
    book_count = 0
    for page in range(settings.start_page, settings.end_page):
        try:
            book_ids = get_id(page)
            for book_id in book_ids:
                download_url = 'https://tululu.org/txt.php'
                payload = {'id': book_id}
                try:
                    book_detail = get_book_details(book_id)
                    book_title = get_title(book_detail, book_id)
                    if not settings.skip_txt:
                        book_path = download_txt(download_url, payload, book_title)
                    else:
                        book_path = ''
                    if not settings.skip_imgs:
                        book_cover = download_cover(get_cover(book_detail))
                    else:
                        book_cover = ''
                    about_book_json = {
                        'title': book_title,
                        'author': get_autor(book_detail),
                        'book_path': f'{book_path}',
                        'image': f'{book_cover}',
                        'comments': get_comments(book_detail),
                        'genres': get_genres(book_detail)
                    }
                    with open("library/about_books.json", "a", encoding='utf8') as my_file:
                        json.dump(about_book_json, my_file, ensure_ascii=False)
                    if settings.json_path:
                        print('Результаты добавлены в "/library/about_books.json"')
                    book_count += 1
                    if settings.dest_folder:
                        print(f'Cкачано книг {book_count}, результаты в каталоге "/library/"')
                    else:
                        print(f'Обработка страницы {page}, скачано книг {book_count}')
                except requests.exceptions.HTTPError as error:
                    print(f'Ошибка сайта на id {book_id}: {error}')
                    continue
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка сайта на странице {page}: {error}')
            continue


if __name__ == '__main__':
    main()
