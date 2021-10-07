from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True)
    native = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    geoname_id = models.IntegerField(unique=True)
    capital = models.CharField(max_length=100, null=True)
    languages = models.ManyToManyField(Language)
    country_flag = models.CharField(max_length=100, null=True)
    country_flag_emoji = models.CharField(max_length=100, null=True)
    country_flag_emoji_unicode = models.CharField(max_length=100, null=True)
    calling_code = models.CharField(max_length=100, null=True)
    is_eu = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.geoname_id)


class Geolocation(models.Model):
    ip = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, null=True)
    continent_code = models.CharField(max_length=100, null=True)
    continent_name = models.CharField(max_length=100, null=True)
    country_code = models.CharField(max_length=100, null=True)
    country_name = models.CharField(max_length=100, null=True)
    region_code = models.CharField(max_length=100, null=True)
    region_name = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Geolocation for IP: {self.ip}"
