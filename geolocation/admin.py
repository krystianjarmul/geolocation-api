from django.contrib import admin

from .models import (
    Language, Currency, Connection, TimeZone, Location, Geolocation
)

admin.site.register(Language)
admin.site.register(Currency)
admin.site.register(Connection)
admin.site.register(TimeZone)
admin.site.register(Location)
admin.site.register(Geolocation)
