import requests
import re
import json
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
    books = soup.find_all(class_='d_book')
    book_hrefs = [book.find('a')['href'] for book in books]
    book_ids = [int(re.sub('/|b', '', href)) for href in book_hrefs]
    return book_ids


def main():
    book_count = 0
    for i in range(1, 11):
        try:
            book_ids = get_id(i)
            for book_id in book_ids:
                download_url = 'https://tululu.org/txt.php'
                payload = {'id': book_id}
                try:
                    book_detail = get_book_details(book_id)
                    book_title = get_title(book_detail, book_id)
                    book_path = download_txt(download_url, payload, book_title)
                    book_cover = download_cover(get_cover(book_detail))
                    about_book_json = {
                        'title': book_title,
                        'author': get_autor(book_detail),
                        'book_path': f'{book_path}',
                        'image': f'{book_cover}',
                        'comments': get_comments(book_detail),
                        'genres': get_genres(book_detail)
                    }
                    with open("about_books.json", "a", encoding='utf8') as my_file:
                        json.dump(about_book_json, my_file, ensure_ascii=False)
                    book_count += 1
                    print(book_count)
                except requests.exceptions.HTTPError as error:
                    print(f'Ошибка сайта на id {book_id}: {error}')
                    continue
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка сайта на странице {i}: {error}')
            continue


if __name__ == '__main__':
    main()
