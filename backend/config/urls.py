from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.auth.api import router as auth_router
from apps.sensors.api import router as sensors_router

api = NinjaAPI(title="Sensor Readings API", version="1.0.0")

api.add_router("/auth/", auth_router, tags=["Authentication"])
api.add_router("/sensors/", sensors_router, tags=["Sensors"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
