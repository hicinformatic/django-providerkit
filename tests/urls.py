"""URL configuration for testing django-providerkit."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
    path("admin/", admin.site.urls),
    path("djproviderkit/", include("djproviderkit.urls")),
]

# admin.site.site_header = "Django ProviderKit - Administration"
# admin.site.site_title = "Django ProviderKit Admin"
# admin.site.index_title = "Welcome to Django ProviderKit"
