import os
import sys
import datetime
from bson import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.helpers import patch_mongo_complex_fields

class CustomDatetime(datetime.datetime):
    pass

def test_patch_basic_types():
    record = {
        '_id': ObjectId('64f8c2c2c2c2c2c2c2c2c2c2'),
        'created': datetime.datetime(2024, 1, 1, 0, 0),
        'name': 'example',
    }
    patched = patch_mongo_complex_fields(record.copy())
    assert isinstance(patched['_id'], str)
    assert isinstance(patched['created'], str)
    assert patched['name'] == 'example'

def test_patch_subclassed_datetime():
    record = {'date': CustomDatetime(2024, 1, 1, 0, 0)}
    patched = patch_mongo_complex_fields(record.copy())
    assert isinstance(patched['date'], str)

