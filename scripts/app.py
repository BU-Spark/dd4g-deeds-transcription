import os
import streamlit as st
from datetime import datetime
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
CLOUD_ID = os.getenv("CLOUD_ID")

# Connect to Elasticsearch
client = Elasticsearch(
    CLOUD_ID,
    api_key=ELASTIC_API_KEY
)
INDEX_NAME = "land_deeds"

# Streamlit UI
st.title("📖 Historical Document Search")
st.sidebar.header("Search Filters")

# Search input and filters
query = st.text_input("Enter search term:")
search_field = st.sidebar.selectbox(
    "Search in:",
    # ["Full Text", "Grantors", "Grantees", "Execution Date", "Recording Date"]
    ["Full Text", "Grantors", "Grantees", "Document Type", "City", "County", "Execution Date", "Recording Date"]
)
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

search_type = st.sidebar.radio("Search Type:", ["Match", "Fuzzy Match"])

# Build Elasticsearch query
def build_query(query, search_field, start_date, end_date, search_type):
    search_fields_mapping = {
        "Full Text": "document_text",
        "Grantors": "grantors",
        "Grantees": "grantees",
        "Document Type": "document_type",
        "City": "city",
        "County": "county",
        "Execution Date": "execution_date",
        "Recording Date": "recording_date"
    }
    
    if search_type == "Match":
        search_filter = {"query": {"match": {search_fields_mapping[search_field]: query}}} if query else {"query": {"match_all": {}}}
    else:  # Fuzzy Match
        search_filter = {"query": {"fuzzy": {search_fields_mapping[search_field]: {"value": query, "fuzziness": "AUTO"}}}} if query else {"query": {"match_all": {}}}
    
    # Date filtering (set range between 1720-1780)
    date_filter = {"range": {search_fields_mapping[search_field]: {
        "gte": "1720-01-01",
        "lte": "1780-12-31"
    }}}
    
    if start_date or end_date:
        if start_date:
            date_filter["range"][search_fields_mapping[search_field]]["gte"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            date_filter["range"][search_fields_mapping[search_field]]["lte"] = end_date.strftime("%Y-%m-%d")
        search_filter["query"] = {"bool": {"must": [search_filter["query"], date_filter]}}
    
    return search_filter

# Perform search
if st.button("Search"):
    query_body = build_query(query, search_field, start_date, end_date, search_type)
    # response = client.search(index=INDEX_NAME, body=query_body)
    response = client.search(index=INDEX_NAME, body=query_body, size=10000)
    
    # Display results
    if response["hits"]["hits"]:
        st.write(f"### {len(response['hits']['hits'])} Results Found:")
        # show_all = st.checkbox("Show All Results")
        # results_to_show = response["hits"]["hits"] if show_all else response["hits"]["hits"][:20]
        for hit in response["hits"]["hits"]:
            doc_id = hit['_source']['document_id']
            with st.expander(f"📜 Document ID: {doc_id}"):
                st.image(f"1/{doc_id}.TIF", caption=f"Document Image {doc_id}")
                st.write(f"**📜 Document Type:** {hit['_source'].get('document_type', 'N/A')}")
                st.write(f"**🖊 Grantors:** {hit['_source'].get('grantors', 'N/A')}")
                st.write(f"**🖊 Grantees:** {hit['_source'].get('grantees', 'N/A')}")
                st.write(f"**🖊 Legal Authorities:** {hit['_source'].get('legal_authorities', 'N/A')}")
                st.write(f"**📍  Acreage:** {hit['_source'].get('acreage', 'N/A')}")
                st.write(f"**📍  Lot Information:** {hit['_source'].get('lot_info', 'N/A')}")
                st.write(f"**📍  City:** {hit['_source'].get('city', 'N/A')}")
                st.write(f"**📍  County:** {hit['_source'].get('county', 'N/A')}")
                st.write(f"**📅 Execution Date:** {hit['_source'].get('execution_date', 'N/A')}")
                st.write(f"**📅 Recording Date:** {hit['_source'].get('recording_date', 'N/A')}")
                # st.write(f"**📖 Document Text:** {hit['_source']['document_text'][:500]}...")  # Truncate long text
                st.write(f"**📖 Document Text:** {hit['_source']['document_text']}")
                st.write("---")
    else:
        st.write("No results found.")