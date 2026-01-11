from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _
from providerkit.kit import FIELDS_PROVIDER_BASE
from providerkit.kit.config import FIELDS_CONFIG_BASE
from providerkit.kit.package import FIELDS_PACKAGE_BASE
from providerkit.kit.service import FIELDS_SERVICE_BASE
from virtualqueryset.models import VirtualModel

from djproviderkit import fields_associations
from djproviderkit.managers.provider import ProviderManager

FIELDS_PROVIDERKIT = {
    **FIELDS_PROVIDER_BASE,
    **FIELDS_CONFIG_BASE,
    **FIELDS_PACKAGE_BASE,
    **FIELDS_SERVICE_BASE,
}

name_config: dict[str, Any] = FIELDS_PROVIDER_BASE['name']


class ProviderModel(VirtualModel):
    """Virtual model for providers."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=name_config['label'],
        help_text=name_config['description'],
        primary_key=True,
    )

    objects = ProviderManager()

    class Meta:
        managed = False
        abstract = True
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def __str__(self) -> str:
        return str(self.name)


for field, value in FIELDS_PROVIDERKIT.items():
    if field == 'name':
        continue

    db_field = fields_associations[value['format']](
        verbose_name=value['label'], help_text=value['description']
    )

    ProviderModel.add_to_class(field, db_field)
