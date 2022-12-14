import json
import argparse
from more_itertools import chunked
from pathlib import Path
from urllib.parse import quote
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def rebuild(db_path):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open(db_path, "r", encoding='utf8') as books:
        book_descriptions = json.load(books)
    books = []
    for book_description in book_descriptions:
        if book_description['image'] != 'Обложка отсутствует':
            book = {
                'image': book_description['image'].replace('\\', '/'),
                'title': book_description['title'],
                'author': book_description['author'],
                'book_path': quote(book_description['book_path'].replace('\\', '/')),
                'genres': ', '.join(book_description['genres'])
            }
        else:
            book = {
                'image': 'static/nopic.gif',
                'title': book_description['title'],
                'author': book_description['author'],
                'book_path': quote(book_description['book_path'].replace('\\', '/')),
                'genres': ', '.join(book_description['genres'])
            }
        books.append(book)

    books_on_page = 20
    chunked_books = list(chunked(books, books_on_page))
    pages = [{
        'page_number': page,
    } for page in range(1, (len(chunked_books) + 1))]

    for page, books_chunk in enumerate(chunked_books, 1):
        rendered_page = template.render(books=books_chunk, sheets=pages, page=page, max_page=pages[-1]['page_number'])
        Path('pages').mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Input DB file path')
    parser.add_argument('db_path', nargs='?', type=str, default="library/about_books.json")
    db_path = parser.parse_args().db_path

    rebuild(db_path)
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')
