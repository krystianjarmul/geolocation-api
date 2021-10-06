from rest_framework import routers

from .views import GeolocationViewSet

app_name = "geolocation"

router = routers.DefaultRouter()
router.register("geolocations", GeolocationViewSet, basename="geolocation")
urlpatterns = router.urls
