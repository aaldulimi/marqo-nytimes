import streamlit as st
import marqo
from marqo_nytimes.load import load
from dataclasses import asdict


def build_index(name, filename, max_count):
    mq = marqo.Client(url='http://localhost:8882')
    index = mq.index(name)

    load_documents = load(filename)

    i = 0 
    for doc in load_documents:
        index.add_documents([asdict(doc)])
        i += 1

        # set fixed amount of docs to index, indexing can take sometime depending on the machine
        if i > max_count: break

    return index
    


if __name__ == "__main__":
    st.title("NYTimes Tensor search using Marqo!")
    st.write("Tensor search on articles published by NYTimes within the last week.")

    col1, col2 = st.columns(2)

    search_field = col1.selectbox("Choose field to search", ["title", "body", "author"])
    results_count = col2.slider("Number of results to show", 1, 10, 5)

    index = build_index("nytimes-index", "data/data.xml", 100)

    search_query = st.text_input("Search", placeholder="Did Putin say something?")
    
    if search_query:
        results = index.search(search_query, searchable_attributes=[search_field])
           
        for result in results["hits"][:results_count]:
            st.write(result["title"])
            st.caption(result["url"])
    