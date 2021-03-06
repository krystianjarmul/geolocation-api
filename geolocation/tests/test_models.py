from django.test import TestCase

from geolocation.models import Geolocation, Language
from geolocation.repository import create_geolocation


class GeolocationModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_data = dict(
            ip="134.201.250.155",
            type="ipv4",
            continent_code="NA",
            continent_name="North America",
            country_code="US",
            country_name="United States",
            region_code="CA",
            region_name="California",
            city="Los Angeles",
            zip="90013",
            latitude=34.0453,
            longitude=-118.2413,
            location=dict(
                geoname_id=5368361,
                capital="Washington D.C.",
                country_flag="https://testwebsitewithflags.com/usa",
                country_flag_emoji="us",
                country_flag_emoji_unicode="U+1F1FA U+1F1F8",
                calling_code="1",
                is_eu=False,
                language=[dict(code="en", name="English", native="English"), ]
            )
        )
        create_geolocation(test_data)

    def test_geolocation_properties(self):
        geolocation = Geolocation.objects.get(id=1)

        self.assertEqual(geolocation.ip, "134.201.250.155")
        self.assertEqual(geolocation.type, "ipv4")
        self.assertEqual(geolocation.continent_code, "NA")
        self.assertEqual(geolocation.continent_name, "North America")
        self.assertEqual(geolocation.country_code, "US")
        self.assertEqual(geolocation.country_name, "United States")
        self.assertEqual(geolocation.region_code, "CA")
        self.assertEqual(geolocation.region_name, "California")
        self.assertEqual(geolocation.city, "Los Angeles")
        self.assertEqual(geolocation.zip, "90013")
        self.assertEqual(geolocation.latitude, 34.0453)
        self.assertEqual(geolocation.longitude, -118.2413)
        self.assertEqual(str(geolocation.location), "5368361")
        self.assertEqual(
            str(geolocation), "Geolocation for IP: 134.201.250.155"
        )


class LanguageModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(code="en", name="English", native="English")

    def test_language_properties(self):
        language = Language.objects.first()

        self.assertEqual(language.code, "en")
        self.assertEqual(language.name, "English")
        self.assertEqual(language.native, "English")
        self.assertEqual(str(language), "English")
