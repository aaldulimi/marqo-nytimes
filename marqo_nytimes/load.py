from marqo_nytimes.document import Document
from lxml import etree

def load(file_location):
    with open(file_location, 'rb') as file:
        article_count = 0

        for _, doc in etree.iterparse(file, events=('end',), tag='doc'):
            article_count += 1
            title = doc.findtext('./title')
            author = doc.findtext('./author')
            body = doc.findtext('./body')
            url = doc.findtext('./url')
            
            yield Document(_id=str(article_count), title=title, author=author, body=body, url=url)
            
            doc.clear()