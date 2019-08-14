from pprint import pprint
#import re
import requests
import json
import pandas as pd

# Задача 1 (Данные о погоде)

#req = requests.get("https://yandex.ru").text
#temp = re.findall("([-+][0-9]+)°",req)
#print(temp)

#cities = ['Moscow', 'Novosibirsk', 'Anapa', 'Kazan', 'Tomsk', 'Vladivostok']
#appid = 'e91a6d9a3c9d15102a89ac457b045ec2'
#main_link = 'http://api.openweathermap.org/data/2.5/weather?'
#for city in cities:
#    link = f'{main_link}q={city}&appid={appid}'
#    req = requests.get(link)
#    data = json.loads(req.text)
#    print(data['name'],data['main']['temp']-273.15)

# Задача 2 (Авиалинии)

#link = 'http://min-prices.aviasales.ru/calendar_preload?'
#origin = 'MOW' #IATA == Moscow -> MOW
#destination = 'LED' #IATA == LED
#link = f'{link}origin={origin}&destination={destination}'
#req = requests.get(link)
#data = json.loads(req.text)
#pprint(data)
#for i in data['best_prices']:
#    print(i['value'],i['depart_date'],i['gate'])

# Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по
# названию города, а не по IATA коду. (У aviasales есть для этого
# дополнительное API) Пункт отправления и пункт назначения должны передаваться
# в качестве параметров. Сделать форматированный вывод, который содержит в себе
# пункт отправления, пункт назначения, дату вылета, цену билета (можно добавить
# еще другие параметры по желанию)

def get_cities():

    link = 'http://api.travelpayouts.com/data/ru/cities.json'

    with requests.session() as s:
        r = s.get(link)

    data = json.loads(r.text)

    cities = dict()

    for item in data:
        cities[item['name']] = item['code']
        cities[item['name_translations']['en']] = item['code']

    return cities

def get_tickets(origin_name, destination_name, one_way_ticket=True):

    cities = get_cities()

    origin = cities.get(origin_name, '--')
    destination = cities.get(destination_name, '--')

    ticket_type = {True: 'true', False: 'false'}

    one_way = ticket_type.get(one_way_ticket, True)

    service = 'http://min-prices.aviasales.ru/calendar_preload?'

    link = f'{service}origin={origin}&destination={destination}&one_way={one_way}'

    with requests.session() as s:
        r = s.get(link)

    data = json.loads(r.text)

    feature_names = ['origin', 'destination', 'depart_date', 'value']

    tickets = pd.DataFrame(data['best_prices'])[feature_names]
    tickets['origin'] = origin_name
    tickets['destination'] = destination_name

    for idx, row in tickets.iterrows():

        print('*' * 36)
        print(f'№:                  {idx+1}')
        print(f'Пункт отправления:  {row[0]}')
        print(f'Пункт назначения:   {row[1]}')
        print(f'Дата отправления:   {row[2]}')
        print(f'Цена билета:        {row[3]}')
        print('*' * 36)
        print('\n')

    return tickets


tickets = get_tickets('Череповец', 'Москва', one_way_ticket=False)