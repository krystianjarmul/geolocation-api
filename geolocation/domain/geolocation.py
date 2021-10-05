import os

import requests

if os.name == "nt":
    from dotenv import load_dotenv

    load_dotenv()


def get_geolocation_data(data):
    ip = data.get("ip")
    base_url = "http://api.ipstack.com/"
    access_key = os.getenv("IPSTACK_ACCESS_KEY")

    response = requests.get(base_url + ip + "?access_key=" + access_key)
    response.json().update(ip=ip)

    return response.json()
