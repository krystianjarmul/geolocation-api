from rest_framework import permissions, generics, mixins
from rest_framework.response import Response
from rest_framework import status

from .models import Geolocation
from .serializers import GeolocationSerializer, PayloadSerializer
from .domain.geolocation import get_geolocation_data
from .repository import create_geolocation


class GeolocationView(
    generics.ListAPIView,
    mixins.CreateModelMixin
):
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        payload_serializer = PayloadSerializer(data=request.data)
        if not payload_serializer.is_valid():
            error_message = {"detail": "IP address is invalid."}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        data = get_geolocation_data(request.data)
        if not data:
            error_message = {"detail": "No data available."}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        geolocation = create_geolocation(data)

        geolocation_serializer = GeolocationSerializer(geolocation)
        return Response(
            geolocation_serializer.data, status=status.HTTP_201_CREATED
        )


class GeolocationDetailView(generics.RetrieveDestroyAPIView):
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "ip"
