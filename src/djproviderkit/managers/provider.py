from typing import Any

from providerkit.helpers import get_providerkit
from virtualqueryset.managers import VirtualManager


class BaseProviderManager(VirtualManager):
    """Base manager for provider models."""

    package_name = 'providerkit'

    def get_data(self) -> list[Any]:
        if not self.model:
            return []

        pvk = get_providerkit()
        providers = pvk.get_providers(lib_name=self.package_name)

        if isinstance(providers, dict):
            providers = list(providers.values())

        return list(providers)


class ProviderManager(BaseProviderManager):
    """Manager for ProviderModel."""

    pass
