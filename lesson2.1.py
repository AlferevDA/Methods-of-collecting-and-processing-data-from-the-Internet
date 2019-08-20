import requests   # библиотека для получения инф. из интернета :)
import re   # библиотека для поиска по полученным данным

import json   # какая-то штука для преобразования

from pprint import pprint   # модуль для более удобного отображения информации (словарь со словарями)

import pandas as pd

# Задача 1 (Данные о погоде)

# Задача 1.1 (Температура воздуха со стартовой страницы "Yandex"
'''
req = requests.get("https://yandex.ru").text
temp = re.findall("([-+][0-9]+)°", req)
print(temp)
'''

# Задача 1.2 (Температура воздуха в указанных городах с ресурса "OpenWeatherMap"
'''
main_link = 'http://api.openweathermap.org/data/2.5/weather?'
appid = 'e91a6d9a3c9d15102a89ac457b045ec2'
cities = ['Moscow', 'Novosibirsk', 'Anapa', 'Kazan', 'Tomsk', 'Vladivostok']

for city in cities:
    link = f'{main_link}q={city}&appid={appid}'
    req = requests.get(link)
    data = json.loads(req.text)
    print(data['name'], data['main']['temp'] - 273.15)
'''

# Задача 2 (Авиалинии)
'''
main_link = 'http://min-prices.aviasales.ru/calendar_preload?'
origin_IATA = 'MOW' #IATA == Moscow -> MOW
destination_IATA = 'LED' #IATA == ‎Saint Petersburg -> LED
link = f'{main_link}origin={origin_IATA}&destination={destination_IATA}'
req = requests.get(link)
data = json.loads(req.text)
pprint(data) # это для изучения того, что нам вытащить
for i in data['best_prices']:
    print(i['value'], i['depart_date'], i['gate'])
'''

# Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по
# названию города, а не по IATA коду. (У aviasales есть для этого
# дополнительное API) Пункт отправления и пункт назначения должны передаваться
# в качестве параметров. Сделать форматированный вывод, который содержит в себе
# пункт отправления, пункт назначения, дату вылета, цену билета (можно добавить
# еще другие параметры по желанию)

origin = input('Город отправления: ')
destination = input('Город прибытия: ')

iata_link = f'https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{origin}%20в%20{destination}'
iata_req = requests.get(iata_link)
iata_data = json.loads(iata_req.text)
origin_IATA = iata_data['origin']['iata']
destination_IATA = iata_data['destination']['iata']

main_link = 'http://min-prices.aviasales.ru/calendar_preload?'
#origin_IATA = 'MOW' #IATA == Moscow -> MOW
#destination_IATA = 'LED' #IATA == ‎Saint Petersburg -> LED
link = f'{main_link}origin={origin_IATA}&destination={destination_IATA}'
req = requests.get(link)
data = json.loads(req.text)

feature_names = ['depart_date', 'value']

tickets = pd.DataFrame(data['best_prices'])[feature_names]

for idx, row in tickets.iterrows():
    print('*' * 36)
    print(f'№:                  {idx+1}')
    print(f'Пункт отправления:  {origin}')
    print(f'Пункт назначения:   {destination}')
    print(f'Дата отправления:   {row[0]}')
    print(f'Цена билета:        {row[1]}')