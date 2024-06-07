import os
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Value must be positive.')


def show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/shows/", filename)


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField(validators=[validate_positive])
    seats_in_row = models.IntegerField(validators=[validate_positive])

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f"{self.user} {self.created_at}"


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    theme = models.ForeignKey(ShowTheme, on_delete=models.SET_NULL, null=True, blank=True, related_name='astronomy_shows')
    image = models.ImageField(null=True, upload_to=show_image_file_path)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name='show_sessions')
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name='show_sessions')
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return f"{self.astronomy_show.title} {self.planetarium_dome.name} {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('row', 'seat', 'show_session')
        ordering = ["row", "seat"]

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {dome_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat} for {self.show_session}"
