from django.db import models
from qualitybase.services.utils import snake_to_camel

from djproviderkit import fields_associations
from djproviderkit.managers.service import ServiceProviderManager


class ServiceProviderModel(models.Model):
    objects = ServiceProviderManager()

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
