from pymongo.collection import Collection
from typing import Dict, Optional


def fetch_records_with_limit_offset(collection: Collection, query: Optional[Dict], limit: int = 0, offset: int = 0):
    cursor = collection.find(query) if query else collection.find()
    

    # Iterate over the cursor to process each document
    for document in cursor:
        yield document


def fetch_records(collection: Collection, query, limit, offset):
    cursor = collection.find(query).skip(offset).limit(limit)

    # Iterate over the cursor to process each document
    for document in cursor:
        yield document
    