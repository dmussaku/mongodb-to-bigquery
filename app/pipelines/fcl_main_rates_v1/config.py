import os
from logger import logger

TEAM_NAME = "pricing"
TEAM_EMAIL = "example@email.com"
DB_CONNECTION_STRING = "mongodb://localhost:27017"
DB_NAME = "local"
DB_COLLECTION = "fclMainRates"
QUERY_LIMIT = 100
QUERY = {}
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "schema.avsc")
