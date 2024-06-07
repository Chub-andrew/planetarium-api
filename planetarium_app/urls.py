from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/planetarium/", include("planetarium_api.urls", namespace="planetarium")),
    path("api/user/", include("user.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', RedirectView.as_view(url='api/planetarium/', permanent=True)), #added this for automative loaded
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
