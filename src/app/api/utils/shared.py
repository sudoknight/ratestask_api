# This file contains utility methods related to data validation and preloading of some parent-child slug regions

import logging
import re
from itertools import groupby
from queue import Empty, Queue
from typing import List

from app.api.utils import crud, queries

logger = logging.getLogger(__name__)

parent_child_slug = {}
ls_ports_codes = []


def is_valid_input(entity: str) -> str:
    """It checks whether the passed port or region identifier is valid or not. It checks for the pressence of prohibited chars.
    If considers all punctuation and space char as invalid with the exclusion of underscore (_)

    Args:
        entity:  It can either be port code or slug
    """
    p = r"[\s]|[^_a-zA-Z]"
    if re.search(p, entity):
        return False
    else:
        return True


def check_if_port(entity: str) -> bool:
    """It checks whether the passed code is a port or not

    Args:
        entity: It can either be port code or slug
    """
    if entity.isupper() and len(entity) == 5:
        return True
    else:
        return False


def is_port_code_exist(code: str) -> bool:
    """Return true if provided port code exists in the database

    Args:
        code: port code to check

    Returns:
        True if found else False
    """
    if code in ls_ports_codes:
        return True
    else:
        return False


def is_slug_exist(slug: str) -> bool:
    """Return true if provided slug exists in the database

    Args:
        code: slug to check

    Returns:
        True if found else False
    """
    if slug in parent_child_slug:
        return True
    else:
        return False


async def get_slug_ports(slug: str) -> List[str]:
    """It returns the list of ports belonging to the slug. Before getting the port it first gets the child regions of the passed slug.
    In case they exist, their ports are also included

    Args:
        slug: input slug for whose ports will be returned
    """
    slugs: list = parent_child_slug[slug]  # get child regions (if available)
    slugs = "','".join(slugs)
    ports = await crud.get(
        queries.get_slug_ports.format(parent_slug=slugs)
    )  # get ports of all slugs

    return [item["code"] for item in ports]


async def load_required_data():
    """This method loads the following:

    * Mapping of slugs and their child slugs {'A': [A, B, C]}  Where B and C are the child slugs of A
    * List of port codes so that they can be used for data validation

    """
    print("Loading data")
    ls_regions = await crud.get(queries.select_region_slugs)
    parent_child = {}  # key is parent region and values are child regions

    def key_func(k):
        return k["parent_slug"]

    for parent_slug_name, group in groupby(ls_regions, key_func):
        group = list(group)
        parent_child[parent_slug_name] = [item["slug"] for item in group]

    global parent_child_slug
    for slug in [item["slug"] for item in ls_regions]:
        parent_child_slug[slug] = find_children_slugs(slug, parent_child)

    logger.info("**Region slugs traversed and stored into memory**")

    global ls_ports_codes
    ls_ports_codes = await crud.get(queries.get_ports_codes)
    ls_ports_codes = [port["code"] for port in ls_ports_codes]
    logger.info("**Ports codes stored into memory**")


def find_children_slugs(slug: str, parent_child: dict) -> list:
    """This method retrieves the child slugs of the passed slug. It iterates and reaches the possible depth of the regions tree.

    # Algorithm:
    If the input region is a parent region (means it has children):
        a. get the children of input region and put them in a queue
        b. Read next child region from the queue:
            a1. add child to the results list
            a2. if this child region has children:
                - Add the children to the queue (so that we can go to the depth of each child)
        c. REPEAT b, untill no more regions are left in the queue

    else:
        d. add the region to the list of results (this region is a leaf region and has no children)

    Args:
        slug: name of the regions for which child regions are required
        parent_child: dict containing parent regions and keys and list of child regions as values

    Returns:
        list containing the child regions of the passed region
    """

    res = []  # stores the child slugs of the passed input slug
    res.append(slug)
    queue = Queue()
    if slug in parent_child:
        child_slugs = parent_child[slug]
        _ = [queue.put(item) for item in child_slugs]

        while (
            True
        ):  # Keep reading next child region from the queue untill no more regions are left in the queue
            try:
                child_slug = queue.get(timeout=0.01)
                res.append(child_slug)

                # get the child slugs if available. So that we can get its children in
                # the next iteration
                if child_slug in parent_child:
                    children = parent_child[child_slug]
                    _ = [queue.put(item) for item in children]

            except Empty as ex1:  # it means we have reached the end of tree for the current region
                print(f"No more children for {slug}: {ex1}")
                break
    return res
