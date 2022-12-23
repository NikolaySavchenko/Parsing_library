import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import unquote
from urllib.parse import urlsplit
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_details(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_title_author(soup_content, book_id):
    book_title = soup_content.select_one('table h1').text.split('::')[0]
    book_author = soup_content.select_one('table h1').text.split('::')[1]
    return {
        'title': f'{book_id}.{sanitize_filename(book_title.strip())}',
        'author': book_author.strip()
    }


def get_cover(soup_content):
    book_cover = soup_content.select_one('table .bookimage img')
    return urljoin('https://tululu.org', book_cover.get("src"))


def get_comments(soup_content):
    book_comments = [(comment.text).strip() for comment in soup_content.select('.texts .black')]
    return book_comments


def get_genres(soup_content):
    genres = [genre.text for genre in soup_content.select('span.d_book a')]
    return genres


def download_txt(url, payload, file_name, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    file_path = Path(f'{folder}/{sanitize_filename(file_name)}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def download_cover(url, folder):
    Path(f'{folder}/image').mkdir(parents=True, exist_ok=True)
    url = unquote(url)
    response = requests.get(url)
    response.raise_for_status()
    cover_name = urlsplit(url).path.split('/')[-1]
    if 'nopic' in cover_name:
        return 'Обложка отсутствует'
    file_path = Path(f'{folder}/image/{cover_name}')
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path
