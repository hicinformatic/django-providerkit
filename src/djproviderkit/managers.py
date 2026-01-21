from typing import Any

from providerkit.helpers import get_providerkit
from virtualqueryset.managers import VirtualManager


class BaseProviderManager(VirtualManager):
    """Base manager for provider models."""

    package_name = 'providerkit'
    _providers_by_name = {}  # Cache des providers par name

    def get_data(self) -> list[Any]:
        if not self.model:
            return []

        pvk = get_providerkit()
        providers = pvk.get_providers(lib_name=self.package_name)

        if isinstance(providers, dict):
            providers = list(providers.values())

        # Stocker les providers dans le cache du manager
        self._providers_by_name.clear()
        for provider in providers:
            self._providers_by_name[provider.name] = provider

        return list(providers)
