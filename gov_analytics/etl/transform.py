import pandas as pd
import numpy as np
from typing import List, Dict
from ..kpis import growth_rate, per_capita
import logging

logger = logging.getLogger(__name__)


def normalize_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def transform_pmay(records: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if df.empty:
        return df
    
    # Try to normalize numeric columns that exist
    possible_cols = ["beneficiaries", "houses_completed", "funds_released"]
    df = normalize_numeric(df, possible_cols)
    
    # Only create derived column if both exist
    if "houses_completed" in df.columns and "beneficiaries" in df.columns:
        df["houses_per_beneficiary"] = df["houses_completed"] / df["beneficiaries"].replace({0: np.nan})
    
    return df


def transform_mnrega(records: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if df.empty:
        return df
    
    possible_cols = ["person_days_generated", "job_cards", "funds_spent"]
    df = normalize_numeric(df, possible_cols)
    
    if "person_days_generated" in df.columns and "job_cards" in df.columns:
        df["person_days_per_job_card"] = df["person_days_generated"] / df["job_cards"].replace({0: np.nan})
    
    return df


def transform_startup(records: List[Dict], population_map: Dict[str, int] = None) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if df.empty:
        return df
    
    possible_cols = ["startups_supported", "funds_allocated"]
    df = normalize_numeric(df, possible_cols)
    
    if population_map and "startups_supported" in df.columns and "state_code" in df.columns:
        df["per_capita_startups"] = df.apply(lambda r: per_capita(r.get("startups_supported"), population_map.get(r.get("state_code"))), axis=1)
    
    return df


def transform_saubhagya(records: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    if df.empty:
        return df
    
    possible_cols = ["households_electrified", "percent_coverage"]
    df = normalize_numeric(df, possible_cols)
    
    return df
