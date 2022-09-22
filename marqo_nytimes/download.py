import requests
from selectolax.parser import HTMLParser
import aiohttp
import asyncio
import xml.etree.ElementTree as ET

URL = "https://www.nytimes.com/sitemap/thisweek/"

header = {
    'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36"  
}

def get_article_url(url):
    all_articles = []

    response = requests.get(url, headers=header)
    data = response.text

    for node in HTMLParser(data).css('div > ul:nth-child(4) > li'):
        if node.child.text() == "Read the document": continue
        article_url = node.child.attrs['href']
        if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue
        
        all_articles.append(article_url)

    return all_articles


async def get_article_data(session, url):
    async with session.get(url, headers=header) as resp:
        response_text = await resp.text()

    
        if response_text:       
            article = HTMLParser(response_text)

            title = article.css_first('h1')
            if title == None: return 
            title = title.text()

            author = article.css_first('span.last-byline')
            if author == None: author = 'unkown' 
            else: author = author.child.text()

            body = ''
            for node in article.css('div.StoryBodyCompanionColumn'):
                paragraph = node.child.select('p').matches
                for p in paragraph:
                    if p: body += p.text()


            print("TITLE: " + title)
            
        return 


async def download_articles(article_urls):
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for url in article_urls[:10]: 
            tasks.append(asyncio.ensure_future(get_article_data(session, url)))
        
        collection = await asyncio.gather(*tasks)



if __name__ == "__main__":
    article_urls = get_article_url(URL)

    asyncio.run(download_articles(article_urls))