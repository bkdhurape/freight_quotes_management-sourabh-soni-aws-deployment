from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from exceptions import BranchException, BranchError ,BranchTransportModeException ,BranchTransportModeError 
from freight.freight_manager import FreightManager
from utils.base_models import StatusBase


class BranchManager(FreightManager):
    """Branch Data manager used for doing db operation."""

    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise BranchException(BranchError.BRANCH_NOT_FOUND)

class BranchTransportManager(FreightManager):
    
    @classmethod
    def find_by(cls, join=False, multi=False, **kwargs):
        try:
            return super().find_by(join, multi, **kwargs)
        except ObjectDoesNotExist:
            raise BranchTransportModeException(BranchTransportModeError.BRANCH_TRANSPORT_MODE_NOT_FOUND)


class BranchServiceManager(models.Manager):

    def delete(self, company_id, branch_id, parent_id):

        # calling branch transport mode inactive and branch inactive function
        self._branch_childrens(branch_id, company_id, parent_id)
        self.delete_branch_transport_mode(branch_id)
        self.inactive_branch(branch_id)
        return True

        
    def _branch_childrens(self, branch_id, company_id, parent_id):

        branch_data = self.model.objects.filter(parent_id=branch_id, company_id=company_id, status=StatusBase.ACTIVE).values()

        if branch_data.count():
            for branch in branch_data:
                self.update_branch_parent(branch['id'], company_id, parent_id)

    def update_branch_parent(self, id, company_id, parent_id):

        branch_update_obj = {}
        branch_update_obj.update(
            {'company': company_id, 'parent': parent_id})
        
        self.model.objects.filter(company_id=company_id, id=id).update(**branch_update_obj)


    def delete_branch_transport_mode(self, branch_id):

        branch_transport_mode_data = apps.get_model('branch', 'BranchTransportMode').objects.filter(status=StatusBase.ACTIVE, branch_id=branch_id)
        
        if branch_transport_mode_data:
            for branch_transport_detail in branch_transport_mode_data:
                branch_transport_detail.delete()


    def inactive_branch(self, branch_id):

        branch_data = self.model.objects.get(id=branch_id)
        branch_data.status = StatusBase.INACTIVE
        branch_data.save()
        


    

        
