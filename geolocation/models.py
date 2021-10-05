from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    native = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    plural = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    symbol_native = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Connection(models.Model):
    asn = models.IntegerField()
    isp = models.CharField(max_length=100)

    def __str__(self):
        return self.isp


class TimeZone(models.Model):
    tz_id = models.CharField(max_length=50)
    current_time = models.DateTimeField(auto_now_add=True)
    gmt_offset = models.IntegerField()
    code = models.CharField(max_length=10)
    is_daylight_saving = models.BooleanField(default=False)

    def __str__(self):
        return self.tz_id


class Location(models.Model):
    geoname_id = models.IntegerField()
    capital = models.CharField(max_length=30)
    languages = models.ManyToManyField(Language)
    country_flag = models.CharField(max_length=100)
    country_flag_emoji = models.CharField(max_length=10)
    country_flag_emoji_unicode = models.CharField(max_length=30)
    calling_code = models.CharField(max_length=10)
    is_eu = models.BooleanField(default=False)

    def __str__(self):
        return str(self.country_flag_emoji).upper()


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
    time_zone = models.ForeignKey(
        TimeZone, on_delete=models.SET_NULL, null=True
    )
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    connection = models.ForeignKey(
        Connection, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"Geolocation for {self.ip}"
