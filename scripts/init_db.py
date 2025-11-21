"""Setup script to initialize database tables"""
from gov_analytics.db import engine, Base
from gov_analytics import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {', '.join(tables)}")
        
    except Exception as e:
        logger.error(f"Failed to create tables: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    init_database()
