from urllib.parse import urlencode
import pymongo
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUV=00D217867419E20F592F662DCC4DE413; IPLOC=CN4403; SUID=B9C776715A18910AAA0000593E3E14; dt_ssuid=6999929200; ssuid=8605198360; start_time=1511610601929; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ABTEST=3|1512908127|v1; weixinIndexVisited=1; ppinf=5|1513762928|1514972528|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTglQkUlODklRTclQTklQkElRTklOUQlOTklRTUlQUYlODJ8Y3J0OjEwOjE1MTM3NjI5Mjh8cmVmbmljazozNjolRTglQkUlODklRTclQTklQkElRTklOUQlOTklRTUlQUYlODJ8dXNlcmlkOjQ0Om85dDJsdUdsamNIV003ekRJa2RNT2VnbzBNa1lAd2VpeGluLnNvaHUuY29tfA; pprdig=pQcgMkc9qTaBP2sjkn_QBsPFP8vXkN7SfEZ7IrcgtbiJ9xqv10prTG2BXJN5j-HvTVScSEJrJ0A7IEQvHr40oSdVqD836v-0fuDO4yS_7jnpSzOkXIO7pHoVRwAmn8Y77JYSXqMoVpWVb58EYyzblBcUmodWY0TgWJa_ZyfJYAY; sgid=07-30468867-AVo6MHAcscibpWAukVU6wOk0; SUIR=1CA55E3C484D2885665AB3EB48A49EB2; usid=-QXbCm2siO5wfOZT; SNUID=2641755C2D2B4EFC23F0506E2E9A4774; ppmdig=1513838388000000a2b9b6a5cf014d19a3bef27298cd1566; sct=10; JSESSIONID=aaazKvb3lpK5y-1eATv8v',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}


proxy = None

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy',proxy)
                count += 1
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)

def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        's_from': input
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(data):
    if db['articles'].update({'title': data['title']},{'$set':data},True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])
def main():
    for page in range(1, 101):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html :
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)

if __name__ == '__main__':
    main()
