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
    text = f.read()
    text_fragments = text.split('#')
    all_wines = []
    for fragment in text_fragments[1:]:
        wine_section = {}
        wine_section['name'] = fragment.strip().split('\n\n')[0]
        wines_in_section = fragment.strip().split('\n\n')[1:]
        wines = []
        for wine in wines_in_section:
            wine = wine.strip().split('\n')
            wine_list = []
            for description in wine:
                description = description.split()
                wine_list.append(' '.join(description[1:]))
            wines.append(wine_list)
            wine_section['wine'] = wines
        all_wines.append(wine_section)
    print(all_wines)

#                 dict_key = lambda key_value: key_value[0].lower()
#                 if ':' in description:
#                     key_value = description.split(':')
#                     wine_description[key_value[0].lower()] = key_value[1].strip()
#                 else:
#                     key_value = description.split()
#                     wine_description[key_value[0].lower()] = 'yes'
#             wine_section.append(wine_description)
#         all_wines.append(wine_section)
# print(all_wines)

rendered_page = template.render(
    data_year=datetime.datetime.now().year - 1920,
    wines=all_wines,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
