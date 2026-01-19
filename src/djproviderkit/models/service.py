from django.db import models
from providerkit.kit import FIELDS_PROVIDER_BASE
from providerkit.kit.config import FIELDS_CONFIG_BASE
from providerkit.kit.package import FIELDS_PACKAGE_BASE
from providerkit.kit.service import FIELDS_SERVICE_BASE
from qualitybase.services.utils import snake_to_camel

from djproviderkit import fields_associations
from djproviderkit.managers import BaseProviderManager

FIELDS_PROVIDERKIT = {
    **FIELDS_PROVIDER_BASE,
    **FIELDS_CONFIG_BASE,
    **FIELDS_PACKAGE_BASE,
    **FIELDS_SERVICE_BASE,
}


class ServiceProviderModel(models.Model):
    objects = BaseProviderManager()

    class Meta:
        managed = False
        abstract = True


def create_service_provider_model(name, fields, app_label, field_id):
    attrs = {
        '__module__': __name__,
        'Meta': type('Meta', (), {'app_label': app_label}),
    }

    fields_to_add = {
        field: fields_associations[cfg['format']](
            verbose_name=cfg['label'],
            help_text=cfg['description'],
            primary_key=field == field_id,
        )
        for field, cfg in fields.items()
    }

    attrs.update(fields_to_add)
    model_name = snake_to_camel(name) + 'ServiceProviderModel'

    return type(model_name, (ServiceProviderModel,), attrs)


def define_provider_fields(primary_key="id"):
    def decorator(cls):
        for field, value in FIELDS_PROVIDERKIT.items():
            if field == primary_key:
                continue
            db_field = fields_associations[value['format']](
                verbose_name=value['label'], help_text=value['description']
            )
            cls.add_to_class(field, db_field)
        return cls
    return decorator

class ServiceProperty:
    """Property descriptor with admin attributes."""

    def __init__(self, func, short_description: str, boolean: bool = False):
        self.func = func
        self.short_description = short_description
        self.boolean = boolean

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)


def define_service_fields(services: list[str]):
    def decorator(cls):
        fields_service = []
        fields_cost = []
        for service in services:
            def make_has_service(svc: str):
                def has_service(self):
                    if not self.services or svc not in self.services:
                        return False
                    missing = self.missing_services or []
                    return svc not in missing

                return ServiceProperty(has_service, f"Has {svc}", boolean=True)

            def make_cost_service(svc: str):
                def cost_service(self):
                    cost = getattr(self, f"cost_{svc}", None)
                    if cost is None or cost == 0 or cost == "free":
                        return "-"
                    return f"${cost:.5f}"

                return ServiceProperty(cost_service, f"Cost {svc}")

            fields_service.append(f"has({service})")
            cls.add_to_class(f"has({service})", make_has_service(service))

            fields_cost.append(f"cost({service})")
            cls.add_to_class(f"cost({service})", make_cost_service(service))

        cls.add_to_class("has_service_fields", fields_service)
        cls.add_to_class("cost_service_fields", fields_cost)
        return cls
    return decorator
