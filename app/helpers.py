import datetime, json
from typing import Dict, Tuple, Optional

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from fastavro import parse_schema


def get_avro_schema(path: str) -> Dict:
    """Gets avro schema from a file"""
    with open(path, "r") as f:
        schema = json.loads(f.read())
    return parse_schema(schema)


def setup_database(
    db_connection_uri: str, db_name: str, collection_name: str
) -> Collection:
    cli = MongoClient(db_connection_uri)
    db = cli.get_database(db_name)
    collection = db.get_collection(collection_name)
    return collection


def fetch_records(collection: Collection, query: Dict, limit: int, offset: int):
    cursor = collection.find(query).skip(offset).limit(limit)

    # Iterate over the cursor to process each document
    for document in cursor:
        yield document


def patch_mongo_complex_fields(
    record: Dict, types: Optional[Tuple] = (ObjectId, datetime.datetime)
):
    """Patches mongo complex fields to be json serializable, casts str on those fields"""
    for key, value in record.items():
        if type(value) in types:
            record[key] = str(value)
    return record
