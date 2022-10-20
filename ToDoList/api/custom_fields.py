from rest_framework.relations import RelatedField
from rest_framework.serializers import SlugRelatedField

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str


class ShowFieldChangeSlugFieldRelatedField(SlugRelatedField):
    """
    A read-write field that represents the target of the relationship
    by field in target of the relationship but can it is changed by slug_field.
    if show_value is None then use __str__ of object
    """

    def __init__(self, show_value=None, **kwargs):
        self.show_value = show_value
        super().__init__(**kwargs)

    def to_representation(self, obj):
        # only changed to represent value not slug_field
        if self.show_value:
            return getattr(obj, self.show_value)
        else:
            return str(obj)
