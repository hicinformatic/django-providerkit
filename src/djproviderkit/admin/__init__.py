from django.conf import settings
from django.contrib import admin
from providerkit.providers.base import ProviderListBase
from qualitybase.services.utils import snake_to_camel

from djproviderkit import models
from djproviderkit.models import ProviderkitModel, ProviderServiceModel

from .provider import BaseProviderAdmin
from .service import ProviderServiceAdmin

services_admins = []
if "djproviderkit" in settings.INSTALLED_APPS:
    admin.site.register(ProviderkitModel, BaseProviderAdmin)
    admin.site.register(ProviderServiceModel, ProviderServiceAdmin)

__all__ = ['BaseProviderAdmin', ]
