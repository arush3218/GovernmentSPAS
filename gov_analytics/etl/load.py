from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging
from typing import List, Dict, Type

logger = logging.getLogger(__name__)


def upsert_records(db: Session, model: Type, records: List[Dict]):
    """Simple bulk upsert: naive implementation that inserts records.

    For production, implement ON CONFLICT upsert or use SQLAlchemy core with
    PostgreSQL-specific conflict resolution.
    """
    objs = [model(**r) for r in records]
    try:
        for o in objs:
            db.merge(o)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Failed to upsert records: %s", e)
