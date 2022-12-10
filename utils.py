import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import unquote
from urllib.parse import urlsplit


def check_for_redirect(response):
    if response.history:
        return True
    else:
        return False


def get_book_details(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    if check_for_redirect(response):
        print(f'Книга с id {book_id} отсутствует!')
        return False
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_autor(soup_content):
    book_author = soup_content.find('table').find('h1').text.split('::')[1]
    return book_author


def get_title(soup_content, book_id):
    book_title = soup_content.find('table').find('h1').text.split('::')[0]
    return f'{book_id}.{sanitize_filename(book_title)}'


def get_cover(soup_content):
    book_cover = soup_content.find('body').find('table').find(class_='bookimage').find('img')['src']
    return f'https://tululu.org/{book_cover}'


def get_comments(soup_content):
    comments = soup_content.find_all(class_='texts')
    book_comments = [comment.find('span', class_='black').text for comment in comments]
    return book_comments


def get_genres(soup_content):
    genres = soup_content.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    return genres


def download_txt(url, payload, file_name, folder='library'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    file_path = Path(f'{folder}/{sanitize_filename(file_name)}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def download_cover(url, folder='library/image'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = unquote(url)
    response = requests.get(url)
    response.raise_for_status()
    cover_name = urlsplit(url).path.split('/')[-1]
    if 'nopic' in cover_name:
        return 'Обложка отсутствует'
    file_path = Path(f'{folder}/{cover_name}')
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path
