"""Custom fields for django-providerkit."""

from django.db import models
from django.forms import Select
from django.utils.translation import gettext_lazy as _

from providerkit.helpers import get_providerkit


class ProviderField(models.CharField):
    """
    CharField storing a provider name, with dynamic choices
    loaded from providerkit at form rendering time.
    """

    def __init__(self, package_name: str | None = None, *args, **kwargs):
        self.package_name = package_name

        kwargs.setdefault("max_length", 100)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("verbose_name", _("Provider"))
        kwargs.setdefault("help_text", _("Select a provider"))

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        Return a form field with dynamically injected choices.
        """
        formfield = super().formfield(**kwargs)

        # Inject dynamic choices at form level (NOT field init)
        choices = self.get_provider_choices()
        formfield.choices = choices
        formfield.widget = Select(choices=choices)

        return formfield

    def get_provider_choices(self):
        """
        Return provider choices as (value, label) tuples.
        Always returns at least the empty choice.
        """
        choices = [("", _("---------"))]

        try:
            pvk = get_providerkit()
            providers = pvk.get_providers(lib_name=self.package_name)

            if isinstance(providers, dict):
                providers = providers.values()

            for provider in providers:
                display_name = getattr(provider, "display_name", None) or provider.name
                choices.append((provider.name, display_name))
        except Exception:
            pass

        return choices