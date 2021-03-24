from django.db import models
from city.models.city import City
from utils.base_models import Base, CreatedUpdatedBy

class Region(Base, CreatedUpdatedBy):
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'regions'

    def __str__(self):
        return self.name