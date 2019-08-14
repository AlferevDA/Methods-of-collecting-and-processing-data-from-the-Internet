import requests
import re
from pprint import pprint
import json
from collections import Counter

def get_link(topic):
    link='https://ru.wikipedia.org/wiki/'+topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html_content = requests.get(link).text
    #with open('new.html','w', encoding='utf-8') as f:
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

# pprint(get_common_words('Футбол')[:10])

# В приложении парсинга википедии получить первую ссылку из раздела "Ссылки" и
# вывести все значимые слова из неё. Результат записать в файл в
# форматированном виде.

def get_first_linked_page(topic, n_words=10):
    html_content = get_topic_page(topic)
    try:
        text = re.findall(r'<li><a rel=.+\sclass=.+\shref=\"https?://\S+?\">', html_content)
        for idx, line in enumerate(text[:1]):
            link = re.findall(r'"((http)s?://.*?)"', line)[0][0]
            try:
                html = requests.get(link, timeout=5).text
                words = re.findall(r'[а-яА-Я]{3,}', html)
                counter = Counter(words)
                most_common_words = dict(counter.most_common(n_words))
                file_name = topic.capitalize() + '_' + '0' * (4 - len(str(idx))) + str(idx+1) + '.json'
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(link)
                with open(file_name, 'a', encoding='utf-8') as f:
                    json.dump(most_common_words, f, ensure_ascii=False)
                print(f'Ссылка №{idx+1}: {link}')
                print(f'{n_words} значимых слов:')
                pprint(most_common_words)
                print(f'Data saved to: {file_name}')
                print('\n')
            except:
                continue
    except:
        pass

#get_first_linked_page('Ломоносов')

# * Научить приложение определять количество ссылок в статье (раздел Ссылки).
# Выполнить поиск слов в статьях по каждой ссылке и результаты записать в
# отдельные файлы.

def get_all_linked_pages(topic, n_words=10):
    html_content = get_topic_page(topic)
    try:
        text = re.findall(r'<li><a rel=.+\sclass=.+\shref=\"https?://\S+?\">', html_content)
        print(f'Кол-во ссылок в статье по теме {topic}: {len(text)}')
        print('\n')
        for idx, line in enumerate(text):
            link = re.findall(r'"((http)s?://.*?)"', line)[0][0]
            try:
                html = requests.get(link, timeout=5).text
                words = re.findall(r'[а-яА-Я]{3,}', html)
                counter = Counter(words)
                most_common_words = dict(counter.most_common(n_words))
                file_name = topic.capitalize() + '_' + '0' * (4 - len(str(idx)))+ str(idx+1) + '.json'
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(link)
                with open(file_name, 'a', encoding='utf-8') as f:
                    json.dump(most_common_words, f, ensure_ascii=False)
                print(f'Ссылка №{idx+1}: {link}')
                print(f'{n_words} значимых слов:')
                pprint(most_common_words)
                print(f'Data saved to: {file_name}')
                print('\n')
            except:
                continue
    except:
        pass

get_all_linked_pages('Ломоносов')