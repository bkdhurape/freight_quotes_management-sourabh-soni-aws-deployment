from freight.custom_lookup_manager import NotEqual

class FreightManager(object):
    """Freight Model Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False,**kwargs):
        q = cls.objects
        if join is True:
            q = q.select_related()
        if multi:
            return q.filter(**kwargs)
        else:
            return q.get(**kwargs)
