import requests
from ..config import settings
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


def fetch_data_from_datagov(resource_id: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Fetch JSON records from data.gov.in API for a given resource id.

    This function expects the data.gov.in API that returns records under a 'records' key.
    The real API may have different structure; adapt resource_id and key accordingly.
    """
    base = "https://data.gov.in/api/datastore/resource.json"
    params = params or {}
    params.update({"resource_id": resource_id, "api-key": settings.DATA_GOV_API_KEY or ""})
    try:
        resp = requests.get(base, params=params, timeout=settings.DEFAULT_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        # common pattern: payload['records'] or payload['data']
        if "records" in payload:
            return payload["records"]
        if "data" in payload:
            return payload["data"]
        # else return full payload if it's a list
        if isinstance(payload, list):
            return payload
        logger.warning("Unexpected payload shape from data.gov.in: keys=%s", list(payload.keys()))
        return []
    except Exception as e:
        logger.exception("Failed to fetch data for resource %s: %s", resource_id, e)
        return []
