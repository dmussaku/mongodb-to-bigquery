import json
from typing import Optional, Dict

from fastavro import writer, reader, parse_schema
from bson.json_util import dumps as bson_dumps
from pymongo import MongoClient
from pymongo.collection import Collection

from config import DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION, logger


def setup_database() -> Collection:
    cli = MongoClient(DB_CONNECTION_STRING)
    db = cli.get_database(DB_NAME)
    collection = db.get_collection(DB_COLLECTION)
    return collection


def fetch_all_records(schema: Dict, collection: Collection, query: Optional[Dict], limit: int = 0, offset: int = 0):
    def fetch_records(collection: Collection, query, limit, offset):
        cursor = collection.find(query).skip(offset).limit(limit)

        # Iterate over the cursor to process each document
        for document in cursor:
            yield document
    
    while True:
        records = list(fetch_records(collection, query, limit, offset))
        
        


with open('schema.json', 'r') as f:
    schema = json.loads(f.read())

