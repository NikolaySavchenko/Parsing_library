import json
import urllib
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

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
print(books[18]['image'])
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
