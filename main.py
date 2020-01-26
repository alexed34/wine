# coding=utf-8
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import os
from dotenv import load_dotenv
import sys
import argparse


def get_file_terminal(path_file_wine):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=path_file_wine)
    namespace = parser.parse_args(sys.argv[1:])
    return namespace


def read_file(filname):
    with open(filname.name, 'r', encoding='utf-8') as f:
        text = f.read()
        return text


def convert_text(text):
    text_fragments = text.split('#')
    all_wines = []
    for fragment in text_fragments[1:]:
        wine_category = {}
        wine_category['name'] = fragment.strip().split('\n\n')[0]
        wines_in_fragment = fragment.strip().split('\n\n')[1:]
        wines = []
        for wine in wines_in_fragment:
            wine_description = wine.strip().split('\n')
            list_wine_characteristics = []
            for characteristics in wine_description:
                characteristics = characteristics.split()
                list_wine_characteristics.append(' '.join(characteristics[1:]))
            wines.append(list_wine_characteristics)
            wine_category['wine'] = wines
        all_wines.append(wine_category)
    print(all_wines)
    return all_wines

# Альтернативная версия конвертации текста
# def convert_text(text):
#     text = text.split('\n')
#     all_wines = []
#     for i in text:
#         if '#' in i:
#             wine_category = {}
#             wine_category['name'] = i.strip('#, , \n')
#             all_wines.append(wine_category)
#             wines = []
#             wine_category['wine'] = wines
#         elif 'Название' in i:
#             list_wine_characteristics = []
#             wines.append(list_wine_characteristics)
#             name = i.split(':')
#             list_wine_characteristics.append(name[1].strip())
#         elif 'Сорт' in i:
#             name = i.split(':')
#             list_wine_characteristics.append(name[1].strip())
#         elif 'Цена' in i:
#             name = i.split(':')
#             list_wine_characteristics.append(name[1].strip())
#         elif 'Картинка' in i:
#             name = i.split(':')
#             list_wine_characteristics.append(name[1].strip())
#         elif 'Выгодное' in i:
#             name = i.split(' ')
#             list_wine_characteristics.append(name[1].strip())
#     print(all_wines)
#     return all_wines


def render_page(env, all_wines):
    template = env.get_template('template.html')
    rendered_page = template.render(
        data_year=datetime.datetime.now().year - 1920,
        wines=all_wines,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    path_file_wine = os.getenv('FILE_WINE')
    namespace = get_file_terminal(path_file_wine)
    text = read_file(namespace)
    all_wines = convert_text(text)
    render_page(env, all_wines)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()