from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet

from planetarium_api.models import ShowTheme, PlanetariumDome

from planetarium_api.serializers import ShowThemeSerializer, PlanetariumDomeSerializer
from rest_framework import viewsets, mixins, status


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
