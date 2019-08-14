import requests
import re
from pprint import pprint

def get_link(topic):
    link='https://ru.wikipedia.org/wiki/'+topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html_content = requests.get(link).text
    #with open('parced_page/new.html','w', encoding='utf-8') as f:
    #    f.write(html_content)
    return html_content

def get_topic_text(topic):
    html_content = get_topic_page(topic)
    words = re.findall('[а-яА-Я]{3,}',html_content)
    return words

def get_common_words(topic):
    word_list = get_topic_text(topic)
    rate={}
    for word in word_list:
        if word in rate:
            rate[word] +=1
        else:
            rate[word] = 1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x: -x[1]) # - это сортировка от большего к меньшему
    return rate_list

pprint(get_common_words('Футбол')[:10])