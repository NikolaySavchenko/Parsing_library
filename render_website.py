import json
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
            }
        else:
            book = {
                'image': 'nopic.gif',
                'title': about_book['title'],
                'author': about_book['author'],
            }
        books.append(book)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilt")


rebuild()

server = Server()

server.watch('template.html', rebuild)

server.serve(root='.')
