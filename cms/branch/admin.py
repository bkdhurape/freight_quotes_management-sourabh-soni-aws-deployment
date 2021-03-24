from django.contrib import admin
from branch.models.branch import Branch
from branch.models.branch_transport_mode import BranchTransportMode

admin.site.register(Branch)
admin.site.register(BranchTransportMode)

