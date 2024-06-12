from django.contrib import admin

from .models import (PlanetariumDome,
                     Reservation,
                     ShowTheme,
                     AstronomyShow,
                     ShowSession,
                     Ticket
                     )

admin.site.register(PlanetariumDome)
admin.site.register(Reservation)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
admin.site.register(Ticket)
