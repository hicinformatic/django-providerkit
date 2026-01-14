from django.contrib import admin
from django_boosted import AdminBoostModel
from qualitybase.services.utils import snake_to_camel


def create_service_provider_admin(name, fields, model=None, **kwargs):
    field_names = list(fields.keys())

    attrs = {
        'list_display': field_names,
        'search_fields': kwargs.get('search_fields', []),
        'readonly_fields': kwargs.get('readonly_fields', []),
        'fieldsets': kwargs.get('fieldsets'),
    }

    admin_name = snake_to_camel(name) + 'ServiceProviderAdmin'

    cls = type(admin_name, (AdminBoostModel,), attrs)

    if model:
        admin.site.register(model, cls)

    return cls
