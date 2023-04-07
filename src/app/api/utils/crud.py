from typing import List

from app.db import database


async def get(query) -> List[dict]:
    """Receives a query string and return list of dicts

    Args:
        query: query string to execute

    Returns:
        result set
    """
    res = [dict(item._mapping) for item in await database.fetch_all(query)]
    return res
