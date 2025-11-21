from typing import List, Type
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


def validate_records(schema: Type, records: List[dict]) -> List[dict]:
    """Validate and coerce records to schema. Returns list of dicts of valid records.

    Invalid records are logged and skipped.
    """
    valid = []
    for i, rec in enumerate(records):
        try:
            obj = schema(**rec)
            valid.append(obj.dict())
        except ValidationError as e:
            logger.warning("Record %s failed validation: %s", i, e)
    return valid
