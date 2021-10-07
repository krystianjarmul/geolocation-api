from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import UserSerializer


class CreateUserTests(APITestCase):

    def test_register_user_successfully(self):
        url = reverse("users:register")
        payload = {"username": "testuser", "password": "testpassword"}

        response = self.client.post(url, payload, format="json")

        user = User.objects.first()
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_register_user_that_already_exists(self):
        payload = {"username": "testuser", "password": "testpassword"}
        User.objects.create_user(**payload)
        url = reverse("users:register")

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_credentials(self):
        payload = {"username": "testuser"}
        url = reverse("users:register")

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
