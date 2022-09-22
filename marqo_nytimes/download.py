import requests
from selectolax.parser import HTMLParser
import random
import xml.etree.ElementTree as ET

URL = "https://www.nytimes.com/sitemap/thisweek/"

headers = {
    'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}'  
}


def get_article_url(url):
    all_articles = []

    response = requests.get(url)
    data = response.text

    for node in HTMLParser(data).css('div > ul:nth-child(4) > li'):
        if node.child.text() == "Read the document": continue
        article_url = node.child.attrs['href']
        if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue
        
        all_articles.append(article_url)

    return all_articles


if __name__ == "__main__":
    article_urls = get_article_url(URL)

    for url in article_urls:
        print(url)