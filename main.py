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
    wines_data = f.read()
    wines_data = wines_data.split('#')
    all_wines = []
    for category in wines_data[1:]:
        name_category = category.strip().split('\n\n')[0]
        wines_category = category.strip().split('\n\n')[1:]
        wine_category = []
        wine_category.append(name_category)
        for wine in wines_category:
            wine = wine.strip().split('\n')
            wine_description = {}
            for description in wine:
                # для проверяющего:
                # здесь я справил ваше замечание с шага 21, но мне кажется код от этого стал хуже
                # вынос в отдельную переменную лямбды  только ухудшает чтение кода, мне так кажется,
                # а более красивое решение мне не приходит в голову.
                dict_key = lambda key_value: key_value[0].lower()
                if ':' in description:
                    key_value = description.split(':')
                    wine_description[dict_key(key_value)] = key_value[1].strip()
                else:
                    key_value = description.split()
                    wine_description[dict_key(key_value)] = 'yes'
            wine_category.append(wine_description)
        all_wines.append(wine_category)
print(all_wines)

rendered_page = template.render(
    data_year=datetime.datetime.now().year - 1920,
    wines=all_wines,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
