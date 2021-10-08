from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("geolocation.urls")),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/users/", include("users.urls")),
    path('api/docs/', include_docs_urls(title="IP Geo API")),
    path(
        "api/schema/",
        get_schema_view(
            title="IPGeoAPI",
            description="API for serving, saving and managing geolocation "
                        "information from provided IP.",
            version="1.0.0"
        ),
        name="openapi-schema"
    )
]
