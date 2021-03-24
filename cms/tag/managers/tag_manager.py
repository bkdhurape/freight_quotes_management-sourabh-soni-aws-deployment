from freight.freight_manager import FreightManager
from django.core.exceptions import ObjectDoesNotExist
from exceptions.tag_exceptions import TagException, TagError

class TagManager(FreightManager):
    """Company Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise TagException(TagError.TAG_NOT_FOUND)

    @classmethod
    def find_by_ids(cls, id):
        if isinstance(id, list):
            return cls.objects.filter(id__in=id)
        else:
            return cls.objects.get(id=id)
