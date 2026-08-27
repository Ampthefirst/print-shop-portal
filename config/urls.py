from django.contrib import admin
from django.urls import path

from apps.core.views import PlaceholderHomeView, healthz

urlpatterns = [
    path("", PlaceholderHomeView.as_view(), name="home"),
    path("healthz/", healthz, name="healthz"),
    path("admin/", admin.site.urls),
]

admin.site.site_header = "Portal administration"
admin.site.site_title = "Portal administration"
admin.site.index_title = "Operations"
