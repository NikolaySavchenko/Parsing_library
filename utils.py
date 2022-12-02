import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(url):
    response = requests.get(url)
    response.raise_for_status()
    if url == response.url:
        return True
    else:
        return False


def get_book_details(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    header = str(soup.find('body').find('table').find('h1'))
    book_name = (header.split('::', maxsplit=1))[0].strip('<h1>').strip()
    book_author = (header.split('title="', maxsplit=1)[1]).split(' - ', maxsplit=1)[0]
    return book_author, f'{id}.{sanitize_filename(book_name)}'


def download_txt(url, file_name, folder='library'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(f'{folder}/{sanitize_filename(file_name)}.txt'), 'wb') as file:
        file.write(response.content)
    return Path(f'{folder}/{sanitize_filename(file_name)}.txt')