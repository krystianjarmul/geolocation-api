from rest_framework import permissions, generics, mixins
from rest_framework.response import Response
from rest_framework import status

from .models import Geolocation, Language, Location
from .serializers import GeolocationSerializer, PayloadSerializer
from .domain.geolocation import get_geolocation_data


class GeolocationView(
    generics.ListAPIView,
    mixins.CreateModelMixin
):
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payload_serializer = PayloadSerializer(data=request.data)
        if not payload_serializer.is_valid():
            error_message = {"detail": "IP address is invalid."}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        data = get_geolocation_data(request.data)
        if not data:
            error_message = {"detail": "No data available."}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

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

        geolocation, _ = Geolocation.objects.get_or_create(
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


class GeolocationDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "ip"

    def get(self, request, *args, **kwargs):
        geolocation = self.get_object()
        serializer = self.get_serializer(geolocation)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        geolocation = self.get_object()

        geolocation.delete()

        return Response(status=status.HTTP_200_OK)
