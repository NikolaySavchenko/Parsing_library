import requests
import re
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from utils import check_for_redirect
from utils import download_txt
from utils import get_book_details
from utils import download_cover
from utils import get_title_author
from utils import get_cover
from utils import get_genres
from utils import get_comments


def get_book_ids(page):
    url = f'https://tululu.org/l55/{page}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.select('.d_book a[href^="/b"]')
    book_ids = {int(re.sub('/|b', '', book['href'])) for book in books}
    return list(book_ids)


def get_max_page():
    url = 'https://tululu.org/l55/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.select('.center a')
    max_page = int(re.sub('/|l55', '', pages[-1]['href']))
    return max_page


def main():
    parser = argparse.ArgumentParser('Input start page, end page and other settings')
    parser.add_argument('start_page', nargs='?', type=int, default=1)
    parser.add_argument('end_page', nargs='?', type=int, default=(get_max_page() + 1))
    parser.add_argument('--dest_folder', type=str, default='library')
    parser.add_argument('--skip_imgs', type=bool, default=False)
    parser.add_argument('--skip_txt', type=bool, default=False)
    parser.add_argument('--json_path', type=str, default='library')
    settings = parser.parse_args()
    book_count = 0
    for page in range(settings.start_page, settings.end_page):
        try:
            book_ids = get_book_ids(page)
            for book_id in book_ids:
                download_url = 'https://tululu.org/txt.php'
                payload = {'id': book_id}
                try:
                    book_detail = get_book_details(book_id)
                    book_title = get_title_author(book_detail, book_id)['title']
                    if not settings.skip_txt:
                        book_path = download_txt(download_url, payload, book_title,
                                                 settings.dest_folder)
                    else:
                        book_path = ''
                    if not settings.skip_imgs:
                        book_cover = download_cover(get_cover(book_detail),
                                                    settings.dest_folder)
                    else:
                        book_cover = ''
                    about_book = {
                        'title': book_title,
                        'author': get_title_author(book_detail, book_id)['author'],
                        'book_path': f'{book_path}',
                        'image': f'{book_cover}',
                        'comments': get_comments(book_detail),
                        'genres': get_genres(book_detail)
                    }
                    Path(settings.json_path).mkdir(parents=True, exist_ok=True)
                    with open(f"{settings.json_path}/about_books.json", "a", encoding='utf8') as my_file:
                        json.dump(about_book, my_file, ensure_ascii=False)
                    book_count += 1
                    print(f'Обработка страницы {page}, cкачано книг {book_count}, '
                          f'результаты в каталоге {settings.dest_folder}')
                    print(f'Информация о книге добавлена в "{settings.json_path}/about_books.json"')
                except requests.exceptions.HTTPError as error:
                    print(f'Ошибка сайта на id {book_id}: {error}')
                    continue
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка сайта на странице {page}: {error}')
            continue


if __name__ == '__main__':
    main()
