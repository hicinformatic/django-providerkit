from django_boosted import AdminBoostModel
from providerkit.kit import FIELDS_PROVIDER_BASE
from providerkit.kit.config import FIELDS_CONFIG_BASE
from providerkit.kit.package import FIELDS_PACKAGE_BASE
from providerkit.kit.service import FIELDS_SERVICE_BASE

FIELDS_PROVIDERKIT = {
    **FIELDS_PROVIDER_BASE,
    **FIELDS_CONFIG_BASE,
    **FIELDS_PACKAGE_BASE,
    **FIELDS_SERVICE_BASE,
}

list_display = list(FIELDS_PROVIDER_BASE.keys())
list_display.append(list(FIELDS_CONFIG_BASE.keys())[-1])
list_display.append(list(FIELDS_PACKAGE_BASE.keys())[-1])
list_display.append(list(FIELDS_SERVICE_BASE.keys())[-1])


class ProviderAdmin(AdminBoostModel):
    """Admin for provider model."""

    list_display = list_display
    search_fields = tuple(FIELDS_PROVIDER_BASE.keys())
    readonly_fields = tuple(FIELDS_PROVIDERKIT.keys())
    fieldsets = [
        (None, {'fields': tuple(FIELDS_PROVIDER_BASE.keys())}),
    ]

    def change_fieldsets(self):
        self.add_to_fieldset('Config', list(FIELDS_CONFIG_BASE.keys()))
        self.add_to_fieldset('Packages', list(FIELDS_PACKAGE_BASE.keys()))
        self.add_to_fieldset('Services', list(FIELDS_SERVICE_BASE.keys()))
