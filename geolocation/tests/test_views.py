from unittest import mock

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from geolocation.models import Geolocation
from geolocation.serializers import GeolocationSerializer
from .factories import (
    GeolocationFactory,
    LanguageFactory,
    LocationFactory,
    faker,
    authenticate_with_jwt
)


class GeolocationAPITests(APITestCase):

    def setUp(self):
        self.language = LanguageFactory.create()
        self.location = LocationFactory.create()
        self.location.languages.add(self.language)
        self.geolocation = GeolocationFactory.create(
            ip="133.11.93.0", location=self.location
        )
        self.user = User.objects.create_user("testuser", "testpassword")

    def test_authenticated_list_geolocations_successfully(self):
        language1 = LanguageFactory.create(code="en")
        location1 = LocationFactory.create(geoname_id=6757145)
        location1.languages.add(language1)
        GeolocationFactory.create(ip="101.0.86.43", location=location1)
        url = reverse("geolocation:geolocation-list",)
        authenticate_with_jwt(self.user, self.client)

        response = self.client.get(url, format="json")

        geolocations = Geolocation.objects.all()
        serializer = GeolocationSerializer(geolocations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_authenticated_retrieve_geolocation_successfully(self):
        url = reverse("geolocation:geolocation-detail", args=["133.11.93.0"])
        authenticate_with_jwt(self.user, self.client)

        response = self.client.get(url, format="json")

        geolocations = Geolocation.objects.get(ip="133.11.93.0")
        serializer = GeolocationSerializer(geolocations)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_authenticated_retrieve_geolocation_not_exists(self):
        url = reverse("geolocation:geolocation-detail", args=["135.13.93.1"])
        authenticate_with_jwt(self.user, self.client)

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("geolocation.views.get_geolocation_data")
    def test_authenticated_create_geolocation_successfully(self, geo_mock):
        geo_mock.return_value = GeolocationSerializer(self.geolocation).data
        url = reverse("geolocation:geolocation-list")
        payload = {"ip": faker.ipv4_public()}
        authenticate_with_jwt(self.user, self.client)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(geo_mock.called)

    def test_authenticated_create_geolocation_ip_is_invalid(self):
        url = reverse("geolocation:geolocation-list")
        payload = {"ip": 12345}
        authenticate_with_jwt(self.user, self.client)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_list_geolocations_unsuccessfully(self):
        url = reverse("geolocation:geolocation-list")

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_retrieve_geolocation_unsuccessfully(self):
        url = reverse("geolocation:geolocation-detail", args=["133.11.93.0"])

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_create_geolocation_unsuccessfully(self):
        url = reverse("geolocation:geolocation-list")
        payload = {"ip": faker.ipv4_public()}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("requests.get", return_value=mock.Mock(status_code=500))
    def test_authenticated_create_geolocation_ipstack_service_unavailable(
            self, request_mock
    ):
        url = reverse("geolocation:geolocation-list")
        payload = {"ip": faker.ipv4_public()}
        authenticate_with_jwt(self.user, self.client)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
