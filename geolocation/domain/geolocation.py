import os
from http import HTTPStatus

import requests
from requests.exceptions import ConnectionError

from core import settings

if os.name == "nt" and settings.DEBUG:
    from dotenv import load_dotenv

    load_dotenv()


def get_geolocation_data(data: dict) -> dict:
    ip = data.get("ip")
    base_url = "http://api.ipstack.com/"
    access_key = os.getenv("IPSTACK_ACCESS_KEY")
    try:
        response = requests.get(base_url + ip + "?access_key=" + access_key)
    except ConnectionError:
        return {}

    if response.status_code != HTTPStatus.OK:
        return {}

    return response.json()
