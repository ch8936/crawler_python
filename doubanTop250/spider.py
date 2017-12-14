import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<li>.*?item.*?(\d+)</em>.*?href="(.*?)".*?title">(.*?)</span>.*?class="bd">.*?"(.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>.*?(\d+).*?&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?average">(\d+.\d+)</span>.*?inq">(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'director': item[3].strip()[34:],
            'actor': item[4].strip()[3:],
            'year': item[5],
            'country': item[6],
            'classification': item[7].strip(),
            'score': item[8],
            'summary': item[9]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(start):
    url = 'http://movie.douban.com/top250?start=' + str(start) + str('&filter=')
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 25 for i in range(10)])
