#from pprint import pprint
#import re
#import requests
#import json
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

from pprint import pprint
import requests
import json
link = 'http://min-prices.aviasales.ru/calendar_preload?'
origin = 'MOW' #IATA == Moscow -> MOW
destination = 'LED' #IATA == LED
link = f'{link}origin={origin}&destination={destination}'
req = requests.get(link)
data = json.loads(req.text)
pprint(data)
for i in data['best_prices']:
    print(i['value'],i['depart_date'],i['gate'])