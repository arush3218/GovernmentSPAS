from prefect import flow, task, get_run_logger
from .etl.extract import fetch_data_from_datagov
from .validation import validate_records
from .schemas import SCHEMAS
from .etl.transform import transform_pmay, transform_mnrega, transform_startup, transform_saubhagya
from .etl.load import upsert_records
from .db import SessionLocal, engine, Base
from . import models
import pandas as pd


@task
def init_db():
    Base.metadata.create_all(bind=engine)
    return True


@task(retries=1)
def extract(resource_id: str):
    logger = get_run_logger()
    logger.info("Extracting resource %s", resource_id)
    return fetch_data_from_datagov(resource_id)


@task
def validate(which: str, records):
    schema = SCHEMAS.get(which)
    if not schema:
        return []
    return validate_records(schema, records)


@task
def transform(which: str, records):
    if which == "pmay":
        return transform_pmay(records).to_dict(orient="records")
    if which == "mnrega":
        return transform_mnrega(records).to_dict(orient="records")
    if which == "startup_india":
        return transform_startup(records).to_dict(orient="records")
    if which == "saubhagya":
        return transform_saubhagya(records).to_dict(orient="records")
    return []


@task
def load(which: str, records):
    db = SessionLocal()
    model = getattr(models, {
        "pmay": "PMAY",
        "mnrega": "MNREGA",
        "startup_india": "StartupIndia",
        "saubhagya": "Saubhagya",
    }[which])
    upsert_records(db, model, records)
    db.close()


@flow
def etl_for_scheme(which: str, resource_id: str):
    init_db()
    raw = extract(resource_id)
    valid = validate(which, raw)
    transformed = transform(which, valid)
    load(which, transformed)
    return {
        "scheme": which,
        "ingested": len(transformed)
    }


@flow
def full_etl_pipeline(config_map: dict):
    results = {}
    for which, rid in config_map.items():
        results[which] = etl_for_scheme(which, rid)
    return results


if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Run ETL flows for government schemes")
    parser.add_argument("--scheme", help="Scheme key (pmay|mnrega|startup_india|saubhagya)")
    parser.add_argument("--resource-id", help="data.gov.in resource id for the scheme")
    parser.add_argument("--config-file", help="Path to JSON file with mapping {scheme: resource_id}")
    args = parser.parse_args()

    if args.scheme and args.resource_id:
        # Run a single scheme flow
        print(f"Running ETL for scheme={args.scheme} resource_id={args.resource_id}")
        etl_for_scheme(args.scheme, args.resource_id)
        sys.exit(0)

    if args.config_file:
        try:
            with open(args.config_file, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
            print(f"Running full ETL using config file: {args.config_file}")
            full_etl_pipeline(cfg)
            sys.exit(0)
        except Exception as e:
            print(f"Failed to load config file: {e}")
            sys.exit(2)

    # Fallback: example dummy resource IDs (replace with real ones)
    cfg = {
        "pmay": "dummy-pmay-resource-id",
        "mnrega": "dummy-mnrega-resource-id",
        "startup_india": "dummy-startup-resource-id",
        "saubhagya": "dummy-saubhagya-resource-id",
    }
    print("No args supplied — running full ETL with example resource IDs (replace with real IDs or use --scheme/--resource-id)")
    full_etl_pipeline(cfg)
