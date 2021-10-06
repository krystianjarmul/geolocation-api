import unittest
from unittest import mock

from geolocation.domain.geolocation import get_geolocation_data


class TestGeolocation(unittest.TestCase):

    def setUp(self) -> None:
        self.request_data = {"ip": "134.201.250.155"}

    @mock.patch("requests.get")
    def test_geolocation_happy_path(self, requests_mock):
        requests_mock.return_value = mock.Mock(
            status_code=200, json=lambda: {"geo": "test_data"}
        )

        data = get_geolocation_data(self.request_data)

        self.assertTrue(requests_mock.called)
        self.assertEqual(data, {"geo": "test_data"})

    @mock.patch("requests.get")
    def test_geolocation_unhappy_path(self, requests_mock):
        requests_mock.return_value = mock.Mock(
            status_code=400, json=lambda: {"geo": "test_data"}
        )

        data = get_geolocation_data(self.request_data)

        self.assertTrue(requests_mock.called)
        self.assertEqual(data, {})
