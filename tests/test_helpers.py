import datetime
import sys
from pathlib import Path
from bson import ObjectId

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.helpers import patch_mongo_complex_fields


def test_patch_mongo_complex_fields_converts_and_preserves_types():
    obj_id = ObjectId("64b55c5e5f5c3a7d2f9c1f42")
    dt = datetime.datetime(2022, 1, 1, 12, 0, 0)
    original = {
        "_id": obj_id,
        "created": dt,
        "name": "test",
        "num": 10,
        "price": 9.99,
        "flag": True,
        "data": {"x": 1},
        "list": [1, 2, 3],
    }

    result = patch_mongo_complex_fields(original)

    assert result is original  # function patches in place
    assert result["_id"] == str(obj_id)
    assert result["created"] == str(dt)

    assert result["name"] == "test"
    assert result["num"] == 10
    assert result["price"] == 9.99
    assert result["flag"] is True
    assert result["data"] == {"x": 1}
    assert result["list"] == [1, 2, 3]
