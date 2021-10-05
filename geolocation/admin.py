from django.contrib import admin

from .models import (Language, Location, Geolocation)

admin.site.register(Language)
admin.site.register(Location)
admin.site.register(Geolocation)
