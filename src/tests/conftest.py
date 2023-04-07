import os
from itertools import groupby
from typing import List

import psycopg2
import pytest
from starlette.testclient import TestClient

import app.api.utils.shared as shared_utils
from app.api.utils import queries
from app.main import app


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
def pre_loaded_data() -> dict:
    """This method loads the following:

    * Mapping of slugs and their child slugs {'A': [A, B, C]}  Where B and C are the child slugs of A
    * List of port codes so that they can be used for data validation

    """

    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    def db_get(query):
        cur.execute(query)
        return [item for item in cur.fetchall()]

    ls_regions = [
        {"slug": item[0], "name": item[1], "parent_slug": item[2]}
        for item in db_get(queries.select_region_slugs)
    ]
    parent_child = {}  # key is parent region and values are child regions
    parent_child_slug = {}

    def key_func(k):
        return k["parent_slug"]

    for parent_slug_name, group in groupby(ls_regions, key_func):
        group = list(group)
        parent_child[parent_slug_name] = [item["slug"] for item in group]

    for slug in [item["slug"] for item in ls_regions]:
        parent_child_slug[slug] = shared_utils.find_children_slugs(slug, parent_child)

    ls_ports_codes = [{"code": item[0]} for item in db_get(queries.get_ports_codes)]
    ls_ports_codes = [port["code"] for port in ls_ports_codes]

    yield {
        "ls_ports_codes": ls_ports_codes,
        "parent_child_rel": parent_child,
        "parent_child_slug": parent_child_slug,
    }


@pytest.fixture(scope="module")
def ls_ports_codes(pre_loaded_data) -> List[str]:
    """It contains the list of port codes in the database

    Yields:
        list of port codes
    """

    yield pre_loaded_data["ls_ports_codes"]


@pytest.fixture(scope="module")
def parent_child(pre_loaded_data):
    yield pre_loaded_data["parent_child_rel"]


@pytest.fixture(scope="module")
def parent_child_slug(pre_loaded_data):
    yield pre_loaded_data["parent_child_slug"]
