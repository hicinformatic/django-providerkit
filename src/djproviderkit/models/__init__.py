from django.utils.translation import gettext_lazy as _
from providerkit.providers.base import ProviderListBase

from .provider import ProviderModel
from .service import create_service_provider_model


class ProviderkitModel(ProviderModel):
    """Model for providerkit."""

    class Meta:
        managed = False
        verbose_name = _('Provider Kit')
        verbose_name_plural = _('Provider Kits')


services_models = []
for svc, cfg in ProviderListBase.services_cfg.items():
    model = create_service_provider_model(svc, cfg['fields'], 'djproviderkit', 'name')
    services_models.append(model)
    globals()[str(model.__name__)] = model

__all__ = ['ProviderModel', 'ProviderkitModel', *[str(model.__name__) for model in services_models]]
