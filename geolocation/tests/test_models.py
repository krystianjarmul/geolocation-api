import datetime

from django.test import TestCase

from geolocation.models import (
    Geolocation, Location, Language, TimeZone, Currency, Connection
)


class TestGeolocationModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_time_zone = TimeZone.objects.create(
            tz_id="America/Los_Angeles",
            current_time=datetime.datetime(2018, 3, 29, 7, 35),
            gmt_offset=-25200,
            code="PDT",
            is_daylight_saving=True
        )
        test_currency = Currency.objects.create(
            code="USD",
            name="US Dollar",
            plural="US dollars",
            symbol="$",
            symbol_native="$"
        )
        test_connection = Connection.objects.create(
            asn=25876, isp="Los Angeles Department of Water & Power"
        )
        test_language = Language.objects.create(
            code="en", name="English", native="English"
        )
        test_location = Location.objects.create(
            geoname_id=5368361,
            capital="Washington D.C.",
            country_flag="https://testwebsitewithflags.com/usa",
            country_flag_emoji="us",
            country_flag_emoji_unicode="U+1F1FA U+1F1F8",
            calling_code="1",
            is_eu=False
        )
        test_location.languages.add(test_language)
        Geolocation.objects.create(
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
            location=test_location,
            time_zone=test_time_zone,
            currency=test_currency,
            connection=test_connection
        )

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
        self.assertEqual(str(geolocation.location), "US")
        self.assertEqual(str(geolocation.time_zone), "America/Los_Angeles")
        self.assertEqual(str(geolocation.currency), "US Dollar")
        self.assertEqual(
            str(geolocation.connection),
            "Los Angeles Department of Water & Power"
        )
        self.assertEqual(
            str(geolocation), "Geolocation for IP: 134.201.250.155"
        )


class TestLanguageModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(code="en", name="English", native="English")

    def test_language_properties(self):
        language = Language.objects.get(id=1)

        self.assertEqual(language.code, "en")
        self.assertEqual(language.name, "English")
        self.assertEqual(language.native, "English")
        self.assertEqual(str(language), "English")
