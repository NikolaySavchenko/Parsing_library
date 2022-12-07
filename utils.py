import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import unquote
from urllib.parse import urlsplit


def check_for_redirect(response):
    if response.history != []:
        return True
    else:
        return False


def get_book_details(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    if check_for_redirect(response):
        return f'Книга с id {book_id} отсутствует!'
    soup = BeautifulSoup(response.text, 'lxml')
    book_title, book_author = soup.find('table').find('h1').text.split('::')
    book_cover = soup.find('body').find('table').find(class_='bookimage').find('img')['src']
    comments = soup.find_all(class_='texts')
    book_comments = [comment.find('span', class_='black').text for comment in comments]
    genres_string = soup.find('span', class_='d_book').find_all('a')
    book_genres = [genre.text for genre in genres_string]

    return {
        'Author': book_author,
        'Title': f'{book_id}.{sanitize_filename(book_title)}',
        'Cover URL': f'https://tululu.org/{book_cover}',
        'All comments': book_comments,
        'Genres': book_genres
            }


def download_txt(url, payload, file_name, folder='library'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if check_for_redirect(response):
        return f'Книга с id {payload["id"]} отсутствует!'
    file_path = Path(f'{folder}/{sanitize_filename(file_name)}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return Path(f'{folder}/{sanitize_filename(file_name)}.txt')


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
    return Path(f'{folder}/{cover_name}')
