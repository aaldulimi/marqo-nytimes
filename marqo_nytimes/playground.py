from dataclasses import asdict
from marqo_nytimes.load import load
import marqo
import pprint 

if __name__ == "__main__":
    mq = marqo.Client(url='http://localhost:8882')
    nytimes_index = mq.index("nytimes-index")

    load_documents = load("data/data.xml")

    for doc in load_documents:
        nytimes_index.add_documents([asdict(doc)])

    results = nytimes_index.search('Did Putin say something?', searchable_attributes=['body'])
    pprint.pprint(results["hits"][0])
