from datetime import datetime
from typing import NamedTuple

import requests
from dateutil.parser import parse as _to_datetime

import config

_api_url = "https://api.personio.de/v1/"


def _token():
    response = requests.post(
        url=_api_url + "auth",
        data={
            "client_id": config.PERSONIO_CLIENT_ID,
            "client_secret": config.PERSONIO_CLIENT_SECRET,
        },
    )
    response.raise_for_status()
    return response.json()["data"]["token"]


class TimeOff(NamedTuple):
    email: str
    first_name: str
    last_name: str
    type_: str
    start_date: datetime
    end_date: datetime
    data: dict


def approved_time_off_for(date_: datetime):
    response = requests.get(
        url=_api_url + "company/time-offs",
        headers={"Authorization": "Bearer {}".format(_token())},
        params={"start_date": date_.isoformat(), "end_date": date_.isoformat(),},
    )
    response.raise_for_status()
    return [
        TimeOff(
            email=to["attributes"]["employee"]["attributes"]["email"]["value"],
            first_name=to["attributes"]["employee"]["attributes"]["first_name"][
                "value"
            ],
            last_name=to["attributes"]["employee"]["attributes"]["last_name"]["value"],
            type_=to["attributes"]["time_off_type"]["attributes"]["name"],
            start_date=(
                _to_datetime(to["attributes"]["start_date"])
                if to["attributes"]["start_date"]
                else None
            ),
            end_date=(
                _to_datetime(to["attributes"]["end_date"])
                if to["attributes"]["end_date"]
                else None
            ),
            data=to["attributes"],
        )
        for to in response.json()["data"]
        if to["attributes"]["status"] == "approved"
    ]


# def time_off_types():
#     response = requests.get(
#         url=_api_url + "company/time-off-types",
#         headers={"Authorization": "Bearer {}".format(_token())},
#     )
#     response.raise_for_status()
#     return response.json()
