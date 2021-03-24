from django.urls import path 
from branch.api.v1.branch_view import  BranchDetailView, BranchView , BranchTransferView 
from branch.api.v1.branch_transport_mode_view import BranchTransportModeView , BranchTransportModeDetailView

urlpatterns = [
    path('', BranchView.as_view()),
    path('<int:branch_id>/', BranchDetailView.as_view()),
    path('reassigned_users/', BranchTransferView.as_view()),
    path('<int:branch_id>/branch_transport_mode/', BranchTransportModeView.as_view()),
    path('<int:branch_id>/branch_transport_mode/<int:id>/',BranchTransportModeDetailView.as_view())

    
]