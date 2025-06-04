from typing import Optional, Dict

from fastavro import parse_schema
from fastavro.validation import validate_many
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
    """Fetch records in batches and validate them against the Avro schema."""
    schema = parse_schema(schema)

    while True:
        records = list(fetch_records(collection, query, limit, offset))
        if not records:
            break

        records = [patch_mongo_complex_fields(record) for record in records]
        logger.info(records)
        validate_many(records, schema)

        if limit:
            offset += limit


def run_pipeline():
    logger.info("Starting pipeline")
    avro_schema = get_avro_schema(SCHEMA_PATH)
    collection = setup_database(DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION)
    logger.info(collection)
    fetch_all_records(
        avro_schema,
        collection,
        query=QUERY,
        limit=QUERY_LIMIT,
        offset=0,
    )
