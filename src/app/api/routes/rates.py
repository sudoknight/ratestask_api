import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query

from app.api.models.rates import RatesSchema
from app.api.utils import crud, queries, shared

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[RatesSchema])
async def get_rates(
    date_from: str = Query(
        regex=r"^[\d]{4}\-[\d]{1,2}\-[\d]{1,2}$",
        default="2016-01-01",
        description="Starting date",
    ),
    date_to: str = Query(
        regex=r"^[\d]{4}\-[\d]{1,2}\-[\d]{1,2}$",
        default="2016-01-10",
        description="Ending date",
    ),
    origin: str = Query(
        min_length=5,
        max_length=20,
        default="CNSGH",
        description="Origin can be port (5-character origin port code) or a slug (A machine-readable form of the region name)",
    ),
    destination: str = Query(
        min_length=5,
        max_length=20,
        default="north_europe_main",
        description="Destination can be port (5-character origin port code) or a slug (A machine-readable form of the region name)",
    ),
):
    """Returns average price per day between those source and destination ports where at least three reocrds are available.
    The source and destination params can either be ports or regions. If any or both of the provided values are region then
    this method will get the port codes and then get prices between soruce and destination port codes.

    **date_from:** Starting date. Defaults to "2016-01-01".\n
    **date_to:** Ending date. Defaults to "2016-01-10".\n
    **origin:** It can be a port or a region. Defaults to "CNSGH".\n
    **destination:** It can be a port or a region. Defaults to "north_europe_main".

    Returns:
        list of averge price per day b/w source and destination enitites
    """

    if not shared.is_valid_input(origin):
        raise HTTPException(
            status_code=422, detail=f"origin contains prohibited characters"
        )

    if not shared.is_valid_input(destination):
        raise HTTPException(
            status_code=422, detail=f"destination contains prohibited characters"
        )

    # if origin is not a port code, handle it as a region slug
    if not shared.check_if_port(origin):
        if shared.is_slug_exist(origin):  # does the slug exist in the database
            origin = await shared.get_slug_ports(
                origin
            )  # if origin in a region slug, get its port codes (including the codes of child regions)

        else:  # if input origin region is not found
            raise HTTPException(
                status_code=404,
                detail=f"origin slug not found in database. Please enter a valid value",
            )
    else:  # if origin is a port
        if shared.is_port_code_exist(origin):
            origin = [origin]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"origin port not found in database. Please enter a valid value",
            )

    # if destination is not a port code, handle it as a region slug
    if not shared.check_if_port(destination):
        if shared.is_slug_exist(destination):  # does the slug exist in the database
            destination = await shared.get_slug_ports(
                destination
            )  # if destination in a region slug, get its port codes (including the codes of child regions)

        else:  # if input destination region is not found
            raise HTTPException(
                status_code=404,
                detail=f"destination slug not found in database. Please enter a valid value",
            )
    else:  # if destination is a port
        if shared.is_port_code_exist(destination):
            destination = [destination]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"destination port not found in database. Please enter a valid value",
            )

    res = await get_prices(date_from, date_to, origin, destination)

    return res


async def get_prices(date_from, date_to, origin, destination) -> List[RatesSchema]:
    query = queries.select_prices.format(
        date_from=date_from,
        date_to=date_to,
        origin="','".join(origin),
        destination="','".join(destination),
    )
    logger.info(query)
    res = await crud.get(query)  # get prices
    return res
