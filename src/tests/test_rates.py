# this file contains unit tests for rates endpoints in routers/rates.py

import logging

import pytest

from app.api.routes import rates
from app.api.utils import shared

logger = logging.getLogger(__name__)


def test_get_rates(test_app, monkeypatch, ls_ports_codes, parent_child_slug):
    """This unit test requests the "/rates" endpoints and evaluates its response against the expected truth.
    It mocks all the database interaction methods. The requests goes through all the validations present in the
    get_rates endpoint.

    Args:
        test_app: Client
        monkeypatch: monkeypatch for mocking
        ls_ports_codes: list of port codes availble in the database (used for validation purposes by the endpoint)
        parent_child_slug: mapping of parent regions and child regions (used for validation and query purposes by the endpoint)

    """
    port_codes = [
        "NLRTM",
        "BEZEE",
        "FRLEH",
        "DEBRV",
        "BEANR",
        "GBFXT",
        "GBSOU",
        "DEHAM",
    ]

    expected_resp = [
        {"day": "2016-01-01", "average_price": 1111.92},
        {"day": "2016-01-02", "average_price": 1112},
        {"day": "2016-01-04", "average_price": None},
        {"day": "2016-01-05", "average_price": 1141.63},
        {"day": "2016-01-06", "average_price": 1141.67},
        {"day": "2016-01-07", "average_price": 1136.96},
        {"day": "2016-01-08", "average_price": 1124.21},
        {"day": "2016-01-09", "average_price": 1124.21},
        {"day": "2016-01-10", "average_price": 1124.25},
    ]

    input_data = "date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

    async def mock_get_prices(date_from, date_to, origin, destination):
        return expected_resp

    async def mock_get_slug_ports(slug):
        return port_codes

    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    monkeypatch.setattr(shared, "ls_ports_codes", ls_ports_codes)

    monkeypatch.setattr(shared, "get_slug_ports", mock_get_slug_ports)
    monkeypatch.setattr(rates, "get_prices", mock_get_prices)

    response = test_app.get(f"/rates/?{input_data}")
    assert response.status_code == 200
    assert response.json() == expected_resp


@pytest.mark.parametrize(
    "date_from, date_to, origin, destination, expected_result",
    [
        [
            "2016-01-01",
            "2016-01-10",
            "CNSGH *",
            "north_europe_main",
            {"detail": "origin contains prohibited characters"},
        ],
        [
            "2016-01-01",
            "2016-01-10",
            "CNSGH",
            "north_europe_main.*",
            {"detail": "destination contains prohibited characters"},
        ],
    ],
)
def test_get_rates_invalid_origin_destination(
    test_app,
    monkeypatch,
    ls_ports_codes,
    parent_child_slug,
    date_from,
    date_to,
    origin,
    destination,
    expected_result,
):
    input_data = f"date_from={date_from}&date_to={date_to}&origin={origin}&destination={destination}"

    async def mock_get_prices(date_from, date_to, origin, destination):
        return {...}

    async def mock_get_slug_ports(slug):
        return [
            "NLRTM",
            "BEZEE",
            "FRLEH",
            "DEBRV",
            "BEANR",
            "GBFXT",
            "GBSOU",
            "DEHAM",
        ]

    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    monkeypatch.setattr(shared, "ls_ports_codes", ls_ports_codes)

    monkeypatch.setattr(shared, "get_slug_ports", mock_get_slug_ports)
    monkeypatch.setattr(rates, "get_prices", mock_get_prices)

    response = test_app.get(f"/rates/?{input_data}")
    assert response.status_code == 422
    assert response.json() == expected_result


@pytest.mark.parametrize(
    "date_from, date_to, origin, destination",
    [
        ["abc", "2016-01-10", "CNSGH", "north_europe_main"],
        [
            "2016-01-01",
            "123",
            "CNSGH",
            "north_europe_main",
        ],
        [
            1680863201.566496,
            "2016-01-10",
            "CNSGH",
            "north_europe_main",
        ],
        [
            "2016-01-10000",
            "2016-01-10",
            "CNSGH",
            "north_europe_main",
        ],
        [
            "2016-100-01",
            "2016-01-10",
            "CNSGH",
            "north_europe_main",
        ],
        [
            "20160-100-01",
            "2016-01-10",
            "CNSGH",
            "north_europe_main",
        ],
    ],
)
def test_get_rates_invalid_dates(
    test_app,
    monkeypatch,
    ls_ports_codes,
    parent_child_slug,
    date_from,
    date_to,
    origin,
    destination,
):
    input_data = f"date_from={date_from}&date_to={date_to}&origin={origin}&destination={destination}"

    async def mock_get_prices(date_from, date_to, origin, destination):
        return {...}

    async def mock_get_slug_ports(slug):
        return [
            "NLRTM",
            "BEZEE",
            "FRLEH",
            "DEBRV",
            "BEANR",
            "GBFXT",
            "GBSOU",
            "DEHAM",
        ]

    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    monkeypatch.setattr(shared, "ls_ports_codes", ls_ports_codes)

    monkeypatch.setattr(shared, "get_slug_ports", mock_get_slug_ports)
    monkeypatch.setattr(rates, "get_prices", mock_get_prices)

    response = test_app.get(f"/rates/?{input_data}")
    assert response.status_code == 422


@pytest.mark.parametrize(
    "date_from, date_to, origin, destination, expected_result",
    [
        [
            "2016-01-01",
            "2016-01-10",
            "CNSGA",
            "north_europe_main",
            {"detail": "origin port not found in database. Please enter a valid value"},
        ],
        [
            "2016-01-01",
            "2016-01-10",
            "scandina",
            "north_europe_main",
            {"detail": "origin slug not found in database. Please enter a valid value"},
        ],
        [
            "2016-01-01",
            "2016-01-10",
            "CNSGH",
            "DKEBB",
            {
                "detail": "destination port not found in database. Please enter a valid value"
            },
        ],
        [
            "2016-01-01",
            "2016-01-10",
            "CNSGH",
            "north_europe",
            {
                "detail": "destination slug not found in database. Please enter a valid value"
            },
        ],
    ],
)
def test_get_rates_unknown_input(
    test_app,
    monkeypatch,
    ls_ports_codes,
    parent_child_slug,
    date_from,
    date_to,
    origin,
    destination,
    expected_result,
):
    input_data = f"date_from={date_from}&date_to={date_to}&origin={origin}&destination={destination}"

    async def mock_get_prices(date_from, date_to, origin, destination):
        return {...}

    async def mock_get_slug_ports(slug):
        return [
            "NLRTM",
            "BEZEE",
            "FRLEH",
            "DEBRV",
            "BEANR",
            "GBFXT",
            "GBSOU",
            "DEHAM",
        ]

    monkeypatch.setattr(shared, "parent_child_slug", parent_child_slug)
    monkeypatch.setattr(shared, "ls_ports_codes", ls_ports_codes)

    monkeypatch.setattr(shared, "get_slug_ports", mock_get_slug_ports)
    monkeypatch.setattr(rates, "get_prices", mock_get_prices)

    response = test_app.get(f"/rates/?{input_data}")
    assert response.status_code == 404
    assert response.json() == expected_result


# # this test is used to test the get end point
# # we mock the get crud method so that we dont send a call to the database
# def test_read_note(test_app, monkeypatch):
#     test_data = {"id": 1, "title": "something", "description": "something else"}

#     async def mock_get(id):
#         return test_data

#     monkeypatch.setattr(crud, "get", mock_get)

#     response = test_app.get("/notes/1")
#     assert response.status_code == 200
#     assert response.json() == test_data


# # this test is used to test the get end point when the input id is invalid
# # we mock the get crud method so that we dont send a call to the database
# def test_read_note_incorrect_id(test_app, monkeypatch):

#     # when the input id is 999
#     test_data = 999

#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(crud, "get", mock_get)

#     response = test_app.get(f"/notes/{test_data}")
#     assert response.status_code == 404  # not found
#     assert response.json()["detail"] == f"Note not found for id {test_data}"

#     # when the input id 0
#     test_data = 0
#     response = test_app.get(f"/notes/{test_data}")
#     assert response.status_code == 422  # validation error


# # This test case is used to test the get all notes endpoint
# # its mocks the get all method so that we don't read all the records from the database
# def test_read_all_notes(test_app, monkeypatch):
#     test_data = [
#         {"title": "something", "description": "something else", "id": 1},
#         {"title": "someone", "description": "someone else", "id": 2},
#     ]

#     async def mock_get_all():
#         return test_data

#     monkeypatch.setattr(crud, "get_all", mock_get_all)
#     response = test_app.get("/notes/")
#     assert response.status_code == 200  # if this cond is false, throw error
#     assert response.json() == test_data  # if this cond is false, throw error


# # This test case is used to test the update end point
# # it mocks the db updated method, and get after updated method.
# def test_update_note(test_app, monkeypatch):
#     test_update_data = {"title": "someone", "description": "someone else", "id": 1}

#     async def mock_get(id):
#         return True

#     monkeypatch.setattr(crud, "get", mock_get)

#     async def mock_put(id, payload):
#         return 1

#     monkeypatch.setattr(crud, "put", mock_put)

#     response = test_app.put("/notes/1/", content=json.dumps(test_update_data))
#     assert response.status_code == 200
#     assert (
#         response.json() == test_update_data
#     )  # if data after updated is not equal to the updated payload


# # the below test case is used to test update end point, when the input payload is invalid
# # In the parametrize decorator, method input params and expected output value are passed for each test.
# @pytest.mark.parametrize(
#     "id, payload, status_code",
#     [
#         [1, {}, 422],  # all required fields missing
#         [1, {"description": "bar"}, 422],  # some required fields missing
#         [999, {"title": "foo", "description": "bar"}, 404],  # id not valid
#         [
#             1,
#             {"title": "1", "description": "bar"},
#             422,
#         ],  # input text not meeting validation rules
#         [
#             1,
#             {"title": "foo", "description": "1"},
#             422,
#         ],  # input text not meeting validation rules
#         [
#             0,
#             {"title": "foo", "description": "bar"},
#             422,
#         ],  # input id not meeting validation rules
#     ],
# )
# def test_update_not_invalid(test_app, monkeypatch, id, payload, status_code):
#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(crud, "get", mock_get)
#     response = test_app.put(
#         f"/notes/{id}/",
#         content=json.dumps(payload),
#     )
#     assert response.status_code == status_code


# # The below test is to check the delete end point
# # it mocks the db crud methods for get and delete.


# def test_remove_note(test_app, monkeypatch):
#     test_data = {"title": "something", "description": "something else", "id": 1}

#     async def mock_get(id):
#         return test_data

#     monkeypatch.setattr(crud, "get", mock_get)

#     async def mock_delete(id):
#         return id

#     monkeypatch.setattr(crud, "delete", mock_delete)

#     response = test_app.delete("/notes/1")
#     assert response.status_code == 200
#     assert response.json() == test_data


# # The below test is to check the delete endpoint when the input id is invalid
# def test_remove_note_incorrec_id(test_app, monkeypatch):

#     # when the input id is 999
#     test_data = 999

#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(crud, "get", mock_get)

#     response = test_app.delete(f"/notes/{test_data}")
#     assert response.status_code == 404
#     assert response.json()["detail"] == f"Note not found for id {test_data}"

#     # when the input id is 0
#     test_data = 0
#     response = test_app.delete(f"/notes/{test_data}")
#     assert response.status_code == 422  # validation error
