from django.db import models
from country.managers.country_manager import CountryManager
from utils.base_models import Base, CreatedUpdatedBy


class Country(Base, CreatedUpdatedBy, CountryManager):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)
    currency_code = models.CharField(max_length=3)

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name
