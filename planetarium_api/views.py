import json
from datetime import datetime

from django.db.models import F, Count
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from planetarium_api.models import ShowTheme, PlanetariumDome, Reservation, \
    ShowSession, AstronomyShow, Ticket
from planetarium_api.permissions import IsAdminOrIsAuthenticateOrReadOnly

from planetarium_api.serializers import (
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    ReservationSerializer,
    ReservationListSerializer, ShowSessionSerializer,
    ShowSessionListSerializer, ShowSessionDetailSerializer,
    AstronomyShowSerializer, AstronomyShowListSerializer, TicketSerializer,
    AstronomyShowDetailSerializer
)
from rest_framework import viewsets, mixins, status


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIsAuthenticateOrReadOnly,)

    def get_permissions(self):
        if self.action in ('list', "retrieve"):
            return (IsAuthenticated(),)

        return super().get_permissions()


class PlanetariumDomeViewSet(
    viewsets.ModelViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AstronomyShow.objects.prefetch_related("theme")
    serializer_class = AstronomyShowSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIsAuthenticateOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the astronomy shows with filters"""
        title = self.request.query_params.get("title")
        theme_ids = self.request.query_params.get("themes")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if theme_ids:
            theme_ids = self._params_to_ints(theme_ids)
            queryset = queryset.filter(theme__id__in=theme_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowDetailSerializer

        return AstronomyShowSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="Filter astronomy shows by title",
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="themes",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter astronomy shows by theme IDs (ex. ?themes=1,2)",
                location=OpenApiParameter.QUERY,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of astronomy shows"""
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show",
        "tickets__show_session__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    # pagination_class = OrderPagination
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects.all()
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIsAuthenticateOrReadOnly,)

    def get_queryset(self):
        date = self.request.query_params.get("date")
        show_id_str = self.request.query_params.get("astronomy_show")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if show_id_str:
            queryset = queryset.filter(astronomy_show_id=int(show_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer

        if self.action == "retrieve":
            return ShowSessionDetailSerializer

        return ShowSessionSerializer

    @action(detail=True, methods=['get'])
    def placement(self, request, pk=None):
        show_session = self.get_object()
        dome = show_session.planetarium_dome
        rows = dome.rows
        seats_in_row = dome.seats_in_row
        tickets = show_session.tickets.all()

        placement = [["-" for _ in range(seats_in_row)] for _ in range(rows)]

        for ticket in tickets:
            row_index = ticket.row - 1
            seat_index = ticket.seat - 1
            placement[row_index][seat_index] = "+"

        return Response({
            "show_session": show_session.id,
            "planetarium_dome": dome.id,
            "seating": placement
        })


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
