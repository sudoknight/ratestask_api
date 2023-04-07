# this file contains unit tests for shared utility methods in utils/shared.py
import pytest

from app.api.utils import crud, shared

pytest_plugins = (
    "pytest_asyncio",
)  # plugin for your async framework in order to handle coroutines


@pytest.mark.parametrize(
    "entity, expected_result",
    [
        ["FRBES", True],
        ["north_europe_main", True],
        ["SEPIT *", False],
        ["scandinavia.*", False],
    ],
)
def test_is_valid_input(entity: str, expected_result: bool):
    assert shared.is_valid_input(entity) == expected_result


@pytest.mark.parametrize(
    "entity, expected_result",
    [
        ["FRBES", True],
        ["GBSSH", True],
        ["north_europe_main", False],
        ["scandinavia", False],
    ],
)
def test_check_if_port(entity: str, expected_result: bool):
    assert shared.check_if_port(entity) == expected_result


@pytest.mark.parametrize(
    "code, expected_result",
    [
        ["DKEBJ", True],
        ["GBSSH", True],
        ["EFGHI", False],
        ["ABCDE", False],
    ],
)
def test_is_port_code_exist(
    monkeypatch, ls_ports_codes, code: str, expected_result: bool
):
    print("----->", ls_ports_codes)
    monkeypatch.setattr(shared, "ls_ports_codes", ls_ports_codes)
    print("----->", ls_ports_codes)
    assert shared.is_port_code_exist(code) == expected_result


@pytest.mark.parametrize(
    "slug, expected_result",
    [
        ["baltic", True],
        ["norway_south_west", True],
        ["norway south west", False],
        ["norway_east_west", False],
    ],
)
def test_is_slug_exist(
    monkeypatch, parent_child_slug, slug: str, expected_result: bool
):
    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    print(parent_child_slug)
    assert shared.is_slug_exist(slug) == expected_result


@pytest.mark.asyncio
async def test_get_slug_ports(monkeypatch, parent_child_slug):

    # these are the ports of scandinavia (including the ports of its child regions)
    test_data = [
        {"code": "NOOSL"},
        {"code": "NOSVG"},
        {"code": "NOMAY"},
        {"code": "SEHAD"},
        {"code": "DKCPH"},
        {"code": "NOFRK"},
        {"code": "NOSKE"},
        {"code": "NOKSU"},
        {"code": "SEMMA"},
        {"code": "NOSVE"},
        {"code": "NOFUS"},
        {"code": "SENRK"},
        {"code": "NOIKR"},
        {"code": "DKFRC"},
        {"code": "NOHVI"},
        {"code": "NOUME"},
        {"code": "SESOE"},
        {"code": "NOHAL"},
        {"code": "NOBVG"},
        {"code": "SEWAL"},
        {"code": "NOFRO"},
        {"code": "SEHEL"},
        {"code": "NOMOL"},
        {"code": "NOTON"},
        {"code": "NODRM"},
        {"code": "NOSAS"},
        {"code": "NOKRS"},
        {"code": "NOSUN"},
        {"code": "DKAAR"},
        {"code": "SEAHU"},
        {"code": "NOBVK"},
        {"code": "NOTOS"},
        {"code": "SEGOT"},
        {"code": "NOTRD"},
        {"code": "NOHAU"},
        {"code": "DKAAL"},
        {"code": "NOMSS"},
        {"code": "FOTHO"},
        {"code": "NOHYR"},
        {"code": "NOTAE"},
        {"code": "SEGVX"},
        {"code": "NOBGO"},
        {"code": "SEOXE"},
        {"code": "NOLAR"},
        {"code": "ISREY"},
        {"code": "ISGRT"},
        {"code": "NOGJM"},
        {"code": "NOORK"},
        {"code": "NOAES"},
        {"code": "SESTO"},
        {"code": "SEPIT"},
        {"code": "DKEBJ"},
    ]
    # these are the expected port codes we should get when we input scandinavia region
    expected_result = [
        "NOOSL",
        "NOSVG",
        "NOMAY",
        "SEHAD",
        "DKCPH",
        "NOFRK",
        "NOSKE",
        "NOKSU",
        "SEMMA",
        "NOSVE",
        "NOFUS",
        "SENRK",
        "NOIKR",
        "DKFRC",
        "NOHVI",
        "NOUME",
        "SESOE",
        "NOHAL",
        "NOBVG",
        "SEWAL",
        "NOFRO",
        "SEHEL",
        "NOMOL",
        "NOTON",
        "NODRM",
        "NOSAS",
        "NOKRS",
        "NOSUN",
        "DKAAR",
        "SEAHU",
        "NOBVK",
        "NOTOS",
        "SEGOT",
        "NOTRD",
        "NOHAU",
        "DKAAL",
        "NOMSS",
        "FOTHO",
        "NOHYR",
        "NOTAE",
        "SEGVX",
        "NOBGO",
        "SEOXE",
        "NOLAR",
        "ISREY",
        "ISGRT",
        "NOGJM",
        "NOORK",
        "NOAES",
        "SESTO",
        "SEPIT",
        "DKEBJ",
    ]

    # **** When correct region is given ****
    inp = "scandinavia"

    async def mocked_get(query):
        return test_data

    monkeypatch.setattr(crud, "get", mocked_get)
    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    assert await shared.get_slug_ports(inp) == expected_result

    # **** When incorrect region is given ****
    with pytest.raises(
        KeyError
    ):  # As the input region is incorrect we should expect an expection to pass the test
        inp = "scandinavia "
        assert await shared.get_slug_ports(inp) == expected_result


@pytest.mark.parametrize(
    "slug, expected_result",
    [
        [
            "china_main",
            [
                "china_main",
                "china_north_main",
                "china_south_main",
                "china_east_main",
            ],
        ],
        ["baltic", ["baltic", "poland_main", "finland_main", "baltic_main"]],
        pytest.param("north_europe_main", [], marks=pytest.mark.xfail),
        pytest.param("northern_europe", [], marks=pytest.mark.xfail),
    ],
)
def test_find_children_slugs(parent_child, slug, expected_result):
    assert shared.find_children_slugs(slug, parent_child) == expected_result
