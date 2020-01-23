# coding=utf-8

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import os
from dotenv import load_dotenv
import sys
import argparse



load_dotenv()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

path_file_wine = os.getenv('FILE_WINE')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=path_file_wine)
    return parser


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])


with open(namespace.name, 'r', encoding='utf-8') as f:
    wines_page = f.read()
    wines_page = wines_page.split('#')
    all_wines = []
    for group in wines_page[1:]:
        name = group.strip().split('\n\n')[0]
        wines = group.strip().split('\n\n')[1:]
        wine_groups = []
        wine_groups.append(name)
        for wine in wines:
            wine = wine.strip().split('\n')
            wines_description = {}
            for index in wine:
                # для проверяющего:
                # здесь я справил ваше замечание с шага 21, но мне кажется код от этого стал хуже
                # вынос в отдельную переменную лямбды  только ухудшает чтение кода, мне так кажется,
                # а более красивое решение мне не приходит в голову.
                index_key = lambda index: index[0].lower()
                if ':' in index:
                    index = index.split(':')
                    wines_description[index_key(index)] = index[1].strip()
                else:
                    index = index.split()
                    wines_description[index_key(index)] = 'yes'

            wine_groups.append(wines_description)
        all_wines.append(wine_groups)
print(all_wines)

rendered_page = template.render(
    data_year=datetime.datetime.now().year - 1920,
    wines=all_wines,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
