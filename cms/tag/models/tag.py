from django.db import models
from company.models.company import Company
from tag.managers.tag_manager import TagManager
from utils.base_models import StatusBase


class Tag(StatusBase, TagManager):
    company = models.ForeignKey(
        Company, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=False, null=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'tags'
        unique_together = (('company', 'name'))

    def __str__(self):
        return self.name
