from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Geolocation, Language, Location
from .serializers import GeolocationSerializer, PayloadSerializer
from .domain.geolocation import get_geolocation_data


class GeolocationViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Geolocation.objects.all()
        serializer = GeolocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        payload_serializer = PayloadSerializer(data=request.data)
        if not payload_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = get_geolocation_data(request.data)
        location_data = data.get("location", {})

        location, _ = Location.objects.get_or_create(
            geoname_id=location_data.get("geoname_id"),
            capital=location_data.get("capital"),
            country_flag=location_data.get("country_flag"),
            country_flag_emoji=location_data.get("country_flag_emoji"),
            country_flag_emoji_unicode=location_data.get(
                "country_flag_emoji_unicode"
            ),
            calling_code=location_data.get("calling_code"),
            is_eu=location_data.get("is_eu"),
        )

        languages = [
            Language.objects.get_or_create(
                code=lang.get("code"),
                name=lang.get("name"),
                native=lang.get("native")
            )[0]
            for lang in location_data.get("languages", [])
        ]

        location.languages.set(languages)

        geolocation = Geolocation.objects.create(
            ip=data.get("ip"),
            type=data.get("type"),
            continent_code=data.get("continent_code"),
            continent_name=data.get("continent_name"),
            country_code=data.get("country_code"),
            country_name=data.get("country_name"),
            region_code=data.get("region_code"),
            region_name=data.get("region_name"),
            city=data.get("city"),
            zip=data.get("zip"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            location=location
        )

        geolocation_serializer = GeolocationSerializer(geolocation)
        return Response(
            geolocation_serializer.data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Geolocation, id=pk)
        serializer = GeolocationSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
