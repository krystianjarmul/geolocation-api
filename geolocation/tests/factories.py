import factory
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken

from geolocation.models import Geolocation, Location, Language

faker = Faker()


def authenticate_with_jwt(user, client):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    code = faker.language_code()
    name = faker.language_name()
    native = faker.language_name()


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    geoname_id = faker.iana_id()
    capital = faker.city()
    country_flag = faker.image_url()
    country_flag_emoji = "PL"
    country_flag_emoji_unicode = "U+1F1F5 U+1F1F1"
    calling_code = faker.country_calling_code()
    is_eu = faker.pybool()


class GeolocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Geolocation

    ip = faker.ipv4_public()
    type = "ipv4"
    continent_code = "EU"
    continent_name = "Europe"
    country_code = faker.country_code()
    country_name = faker.country()
    region_code = "PK"
    region_name = "Subcarpathian"
    city = faker.city()
    zip = faker.postcode()
    latitude = faker.latitude()
    longitude = faker.longitude()
    location = factory.SubFactory(LocationFactory)
