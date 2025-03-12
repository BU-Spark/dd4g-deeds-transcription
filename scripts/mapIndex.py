import os
import re
import json
import streamlit
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch, helpers


def bulk_index(cloud_id: str, api_key: str, index_name: str, csv_path: str):

    # Connect to Elasticsearch Cloud
    client = Elasticsearch(
        cloud_id, api_key = api_key
    ) 
    index_name = index_name
    # Load the dataset
    file_path = csv_path
    df = pd.read_csv(file_path)


    # Check connection
    if client.ping():
        print("Connected to Elasticsearch successfully!")
    else:
        print("Elasticsearch connection failed.")


    # Define index mapping
    mapping = {
        "mappings": {
            "properties": {
                "document_id": {"type": "keyword"},
                "document_text": {"type": "text"},
                "document_type": {"type": "keyword"},
                "grantors": {"type": "text"},
                "grantees": {"type": "text"},
                "legal_authorities": {"type": "text"},
                "acreage": {"type": "text"},
                "boundaries": {"type": "text"},
                "lot_info": {"type": "text"},
                "city": {"type": "text"},
                "county": {"type": "text"},
                "province_colony": {"type": "text"},
                "execution_date": {"type": "date", "format": "yyyy-MM-dd"},
                "recording_date": {"type": "date", "format": "yyyy-MM-dd"}
            }
        }
    }


    # Function to clean and standardize date format
    def clean_date(date_str):
        if pd.isna(date_str) or "Not specified" in str(date_str):
            return None  # Return None for missing or invalid dates
        try:
            return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format
        except ValueError:
            return None  # Return None if format is unrecognized

    # Apply cleaning functions to date columns
    df["Execution Date"] = df["Execution Date"].apply(clean_date)
    df["Recording Date"] = df["Recording Date"].apply(clean_date)

    # Replace NaN values with empty strings where applicable
    df.fillna("", inplace=True)


    # Create index if it doesn't exist
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

    # Prepare documents for bulk indexing
    def generate_docs(df):
        for _, row in df.iterrows():
            yield {
                "_index": index_name,
                "_id": row["Document ID"],
                "_source": {
                    "document_id": row["Document ID"],
                    "document_text": row["Document Text"],
                    "document_type": row["Document Type"],
                    "grantors": row["Grantors"],
                    "grantees": row["Grantees"],
                    "legal_authorities": row["Legal Authorities"],
                    "acreage": row["Acreage"],
                    "boundaries": row["Boundaries"],
                    "lot_info": row["Lot Info"],
                    "city": row["City"],
                    "county": row["County"],
                    "province_colony": row["Province/Colony"],
                    "execution_date": row["Execution Date"],
                    "recording_date": row["Recording Date"]
                }
            }

    # Bulk upload data
    helpers.bulk(client, generate_docs(df))
    print("Data indexed successfully!")