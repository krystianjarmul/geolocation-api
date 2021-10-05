from rest_framework import serializers

from .models import Geolocation, Language, Location


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ("id",)


class LocationSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        exclude = ("id",)


class GeolocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Geolocation
        fields = "__all__"
