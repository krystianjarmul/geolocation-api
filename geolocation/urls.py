from django.urls import path

from .views import GeolocationView, GeolocationDetailView

app_name = "geolocation"

urlpatterns = [
    path(
        "geolocations/", GeolocationView().as_view(), name="geolocation-list"
    ),
    path(
        "geolocations/<str:ip>",
        GeolocationDetailView().as_view(),
        name="geolocation-detail"
    )
]
