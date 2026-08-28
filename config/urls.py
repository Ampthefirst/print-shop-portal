from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("admin/", admin.site.urls),
    # Public pages are last so they never shadow an application route.
    path("", include("apps.pages.urls")),
]

admin.site.site_header = "Portal administration"
admin.site.site_title = "Portal administration"
admin.site.index_title = "Operations"
