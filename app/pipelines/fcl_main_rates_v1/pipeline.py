import json
import os
from typing import Optional, Dict

from fastavro import writer, reader, parse_schema
from fastavro.validation import validate_many
from bson.json_util import dumps as bson_dumps
from pymongo import MongoClient
from pymongo.collection import Collection

from .config import (
    DB_CONNECTION_STRING,
    DB_NAME,
    DB_COLLECTION,
    logger,
    QUERY_LIMIT,
    QUERY,
    SCHEMA_PATH,
)
from helpers import (
    fetch_records,
    setup_database,
    patch_mongo_complex_fields,
    get_avro_schema,
)


def fetch_all_records(
    schema: Dict,
    collection: Collection,
    query: Optional[Dict],
    limit: int = 0,
    offset: int = 0,
):
    """Continuosly polls data by calling fetch_records and validates it agains the avro schema"""
    collection = setup_database(DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION)
    schema = parse_schema(schema)
    while True:
        records = list(fetch_records(collection, query, limit, offset))
        records = [patch_mongo_complex_fields(record) for record in records]
        logger.info(records)
        validate_many(records, schema)
        break


def run_pipeline():
    logger.info("Starting pipeline")
    avro_schema = get_avro_schema(SCHEMA_PATH)
    collection = setup_database(DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION)
    logger.info(collection)
    fetch_all_records(avro_schema, collection, query=QUERY, limit=QUERY_LIMIT, offset=0)
