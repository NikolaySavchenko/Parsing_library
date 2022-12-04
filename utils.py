import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import unquote
from urllib.parse import urlsplit


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
    book_cover = soup.find('body').find('table').find(class_='bookimage').find('img')['src']
    book_comments_html = soup.find_all(class_='texts')
    book_comments = []
    for comment in book_comments_html:
        temp = ((str(comment).split('span'))[1].replace(' class="black">', '')).replace('</', '')
        book_comments.append(temp)
    book_genre = (str(soup.find_all(class_="d_book")[1]).split('title="')[1]).split(' - перейти')[0]
    return (book_author, f'{id}.{sanitize_filename(book_name)}',
            f'https://tululu.org/{book_cover}', book_comments, book_genre)


def download_txt(url, file_name, folder='library'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(f'{folder}/{sanitize_filename(file_name)}.txt'), 'wb') as file:
        file.write(response.content)
    return Path(f'{folder}/{sanitize_filename(file_name)}.txt')


def download_cover(id, folder='library/image'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = unquote(get_book_details(id)[2])
    response = requests.get(url)
    response.raise_for_status()
    cover_name = (urlsplit(url).path).split('/')[-1]
    if 'nopic' in cover_name:
        return 'Обложка отсутствует'
    with open(Path(f'{folder}/{cover_name}'), 'wb') as file:
        file.write(response.content)
    return Path(f'{folder}/{cover_name}')

# print(get_book_details(5))