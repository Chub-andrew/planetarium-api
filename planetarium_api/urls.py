from django.urls import path, include
from rest_framework import routers

from planetarium_api.views import (
    ShowThemeViewSet,
    PlanetariumDomeViewSet, ShowSessionViewSet, AstronomyShowViewSet, ReservationViewSet
)

router = routers.DefaultRouter()
router.register("Show_Theme", ShowThemeViewSet)
router.register("Planetarium_Dome", PlanetariumDomeViewSet)
router.register("Show_Sessions", ShowSessionViewSet)
router.register("Astronomy_Show", AstronomyShowViewSet)
router.register("Reservation", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
