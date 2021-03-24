from django.db import models
from utils.base_models import Base, CreatedUpdatedBy

class Commodity(Base, CreatedUpdatedBy):
    name = models.CharField(max_length=1024)
    
    class Meta:
        db_table = 'commodities'

    def __str__(self):
        return self.name