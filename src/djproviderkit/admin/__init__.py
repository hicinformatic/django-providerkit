from django.contrib import admin
from providerkit.providers.base import ProviderListBase
from qualitybase.services.utils import snake_to_camel

from djproviderkit import models
from djproviderkit.models import ProviderkitModel

from .provider import ProviderAdmin
from .service import create_service_provider_admin


@admin.register(ProviderkitModel)
class ProviderkitAdmin(ProviderAdmin):
    """Admin for providerkit model."""


services_admins = []
for svc, cfg in ProviderListBase.services_cfg.items():
    model_name = snake_to_camel(svc) + 'ServiceProviderModel'
    model = getattr(models, model_name, None)
    if model:
        adm = create_service_provider_admin(
            svc, cfg['fields'], model=model, readonly_fields=list(cfg['fields'].keys())
        )
        services_admins.append(adm)
        globals()[str(adm.__name__)] = adm

__all__ = ['ProviderAdmin', 'ProviderkitAdmin', *[str(adm.__name__) for adm in services_admins]]
