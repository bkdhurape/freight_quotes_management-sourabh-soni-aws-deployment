from django.db import models
from country.models.country import Country
from state.managers.state_manager import StateManager
from utils.base_models import Base, CreatedUpdatedBy

class State(Base, CreatedUpdatedBy, StateManager):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = 'states'

    def __str__(self):
        return self.name