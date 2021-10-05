from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    native = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Location(models.Model):
    geoname_id = models.IntegerField(unique=True)
    capital = models.CharField(max_length=30)
    languages = models.ManyToManyField(Language)
    country_flag = models.CharField(max_length=100)
    country_flag_emoji = models.CharField(max_length=10)
    country_flag_emoji_unicode = models.CharField(max_length=30)
    calling_code = models.CharField(max_length=10)
    is_eu = models.BooleanField(default=False)

    def __str__(self):
        return str(self.geoname_id)


class Geolocation(models.Model):
    ip = models.CharField(max_length=30)
    type = models.CharField(max_length=10)
    continent_code = models.CharField(max_length=10)
    continent_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=10)
    country_name = models.CharField(max_length=30)
    region_code = models.CharField(max_length=10)
    region_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Geolocation for IP: {self.ip}"
