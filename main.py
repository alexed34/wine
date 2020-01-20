# coding=utf-8

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


with open('roza.txt', 'r', encoding='utf-8') as f:
    wine = f.read()
    wine_page = wine.split('#')
    all_wines = []
    for grup in wine_page[1:]:
        name = grup.strip().split('\n\n')[0]
        wines = grup.strip().split('\n\n')[1:]
        wine_groups = []
        wine_groups.append(name)
        for wine in wines:
            wine = wine.strip().split('\n')
            wines_description = {}
            for index in wine:
                try:
                    index = index.split(':')
                    wines_description[index[0].lower()] = index[1].strip()
                except:
                    index = index[0].split()
                    wines_description[index[0].lower()] = 'yes'
            wine_groups.append(wines_description)
        all_wines.append(wine_groups)



rendered_page = template.render(
    data_year=datetime.datetime.now().year - 1920,
    wines=all_wines,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
