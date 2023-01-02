import json
from more_itertools import chunked
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open("library/about_books.json", "r", encoding='utf8') as books:
        books_json = books.read()
    about_books = json.loads(books_json)
    books = []
    for about_book in about_books:
        if about_book['image'] != 'Обложка отсутствует':
            book = {
                'image': about_book['image'].replace('\\', '/'),
                'title': about_book['title'],
                'author': about_book['author'],
                'book_path': about_book['book_path'].replace('\\', '/'),
                'genres': ', '.join(about_book['genres'])
            }
        else:
            book = {
                'image': 'static/nopic.gif',
                'title': about_book['title'],
                'author': about_book['author'],
                'book_path': about_book['book_path'].replace('\\', '/'),
                'genres': ', '.join(about_book['genres'])
            }
        books.append(book)

    books_chunked = list(chunked(books, 20))
    pages = []
    for page, books_chunk in enumerate(books_chunked, 1):
        pages.append({
            'page_number': page,
        })

    for page, books_chunk in enumerate(books_chunked, 1):
        rendered_page = template.render(books=books_chunk, sheets=pages, page=page, max_page=pages[-1]['page_number'])
        Path('pages').mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')
