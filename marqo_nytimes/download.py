import requests
from selectolax.parser import HTMLParser
import aiohttp
import asyncio
import xml.dom.minidom
import xml.etree.ElementTree as ET

URL = "https://www.nytimes.com/sitemap/thisweek/"

HEADER = {
    'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36"  
}

def get_article_url(url):
    all_articles = []

    response = requests.get(url, headers=HEADER)
    data = response.text

    for node in HTMLParser(data).css('div > ul:nth-child(4) > li'):
        if node.child.text() == "Read the document": continue
        article_url = node.child.attrs['href']
        if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue
        
        all_articles.append(article_url)

    return all_articles


async def get_article_data(session, url):
    async with session.get(url, headers=HEADER) as resp:
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


            doc = ET.Element("doc")
            ET.SubElement(doc, "title").text = title
            ET.SubElement(doc, "author").text = author
            ET.SubElement(doc, "body").text = body
            ET.SubElement(doc, "url").text = url

            dom = xml.dom.minidom.parseString(ET.tostring(doc))
            doc = dom.childNodes[0].toprettyxml()

            global to_load, article_count

            article_count += 1
            to_load.append(doc)
            
            # write docs to file, 10 at time 
            if len(to_load) >= 10:
                with open("data/data.xml", 'a') as file:
                    for doc in to_load:
                        file.write(doc)

                    file.close()

                to_load = []

            
            print("Articles scraped so far: ", str(article_count))
            
        return 



async def download_articles(article_urls):
    async with aiohttp.ClientSession(headers=HEADER) as session:
        tasks = []
        for url in article_urls[:300]: 
            tasks.append(asyncio.ensure_future(get_article_data(session, url)))
        
        collection = await asyncio.gather(*tasks)



if __name__ == "__main__":
    to_load = []
    article_count = 0

    article_urls = get_article_url(URL)

    with open("data/data.xml", 'w') as file:
        file.write('<documents>\n')
        file.close()


    asyncio.run(download_articles(article_urls))


    with open("data/data.xml", 'a') as file:
        file.write('</documents>')
        file.close()
