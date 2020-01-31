# coding=utf-8
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import os
from dotenv import load_dotenv
import sys
import argparse


def get_command_line_argument(path_wine_file):
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default=path_wine_file)
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.name


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        return text


def convert_text(text):
    text_fragments = text.split('#')
    all_wines = []
    for fragment in text_fragments[1:]:
        text_blocks = fragment.strip().split('\n\n')
        wine_category = {
            'name': text_blocks[0]
        }
        text_data = text_blocks[1:]
        wines = []
        for data in text_data:
            text_lines = data.strip().split('\n')
            for line in text_lines:
                if 'Название' in line:
                    wine_characteristics = {'Название': line.split(':')[1]}
                elif 'Сорт' in line:
                    wine_characteristics['Сорт'] = line.split(':')[1]
                elif 'Цена' in line:
                    wine_characteristics['Цена'] = line.split(':')[1]
                elif 'Картинка' in line:
                    wine_characteristics['Картинка'] = line.split(':')[1]
                elif 'Выгодное' in line:
                    wine_characteristics['Выгодное'] = line

            wines.append(wine_characteristics)
            wine_category['wines'] = wines
        all_wines.append(wine_category)
    return all_wines


def render_page(env, all_wines):
    template = env.get_template('template.html')
    rendered_page = template.render(
        data_year=datetime.datetime.now().year - 1920,
        wines=all_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    path_wine_file = os.getenv('WINES_FILE')
    namespace = get_command_line_argument(path_wine_file)
    text = read_file(namespace)
    all_wines = convert_text(text)
    render_page(env, all_wines)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
