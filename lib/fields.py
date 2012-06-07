# coding: utf-8
from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor

# derived from http://softwaremaniacs.org/blog/2007/03/07/auto-one-to-one-field/

class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor): # this line just can't be too long, right?
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            rel_obj = self.related.model(**{self.related.field.name: instance})
            rel_obj.save()
            setattr(instance, self.cache_name, rel_obj)
            return rel_obj


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField, которое создает зависимый объект при первом обращении
    из родительского, если он еще не создан.
    '''

    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))
        if not hasattr(cls._meta, 'one_to_one_field') or not cls._meta.one_to_one_field:
            cls._meta.one_to_one_field = self



from south.modelsinspector import add_introspection_rules

rules = [
    (
        (AutoOneToOneField, ), [],
        {
            "to": ["rel.to", {}],
            "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
            "related_name": ["rel.related_name", {"default": None}],
            "db_index": ["db_index", {"default": True}],
        }
    ),
]

# добавляем правила и модуль
add_introspection_rules(rules, ["^lib\.fields\.AutoOneToOneField"])
