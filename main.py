# coding=utf-8
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import os
from dotenv import load_dotenv
import sys
import argparse


def createParser(path_file_wine):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=path_file_wine)
    return parser


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





def main():
    load_dotenv()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    path_file_wine = os.getenv('FILE_WINE')
    parser = createParser(path_file_wine)
    namespace = parser.parse_args(sys.argv[1:])

    text = read_file(namespace)
    all_wines = convert_text(text)


    rendered_page = template.render(
        data_year=datetime.datetime.now().year - 1920,
        wines=all_wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()