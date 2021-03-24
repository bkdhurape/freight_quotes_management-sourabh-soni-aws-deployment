from city.managers.city_manager import CityManager
from django.db import models
from state.models.state import State
from utils.base_models import Base, CreatedUpdatedBy

class City(Base, CreatedUpdatedBy, CityManager):
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name