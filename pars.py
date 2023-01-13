import csv
import json
from bs4 import BeautifulSoup
import requests
import lxml

url = 'https://summercamp.ru/index.php?title=Категория:Игры&pageuntil=%3F%3F%3F%3F%3F-%3F%3F%3F%3F%3F%3F%3F%0AКрест-параллель#mw-pages'
headers = {'Accept': '*/*',
           'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.0.2500 Yowser/2.5 Safari/537.36'}
#
# Достаем ссылку на сайт

req = requests.get(url)
src = req.text

# Записываем файл html

with open ('sc_index2.html', 'w',encoding='utf-8') as file:
    file.write(src)
with open ('sc_index2.html' ,encoding='utf-8') as file:
    src = file.read()
#
soup = BeautifulSoup(src, 'lxml')

# Создаем словарь {'Название игры':'Ссылка на игру'}

all_games_dict = {}
all_games_html = soup.find(class_="mw-content-ltr").find_all('a')
for game in all_games_html:
    game_href = 'https://summercamp.ru'+game.get('href')
    game_name = game.text
    all_games_dict[game_name] = game_href
all_games_dict.pop('')
all_games_dict.pop('следующие 200')

# # создаем json на основе дикта

with open('all_games_dict2.json', 'w', encoding='utf-8') as file:
    json.dump(all_games_dict, file, ensure_ascii=False, indent=4)
with open('all_games_dict2.json', encoding='utf-8') as file:
    all_games = json.load(file)
count = 1

for game_name, game_href in all_games.items():
    sym = ["'", " ", "-", ",",'"','?','!']
    for item in sym:
        if item in game_name:
            game_name = game_name.replace(item, '_')
    req = requests.get(headers=headers, url=game_href)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    game_title = soup.find(class_="firstHeading").find('span')
    title = game_title.text
    game_description = soup.find(class_="mw-content-ltr").find_all('p')
    description = []
    for item in game_description:
        description.append(item.text.strip())
    game_title_desc = {}
    game_title_desc[title] = description
    with open(f'games2/{game_name}.json','w',encoding='utf-8') as file:
        json.dump(game_title_desc,file, ensure_ascii=False, indent=4)
    game_title_desc.clear()





