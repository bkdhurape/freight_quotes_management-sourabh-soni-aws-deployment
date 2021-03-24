from django.urls import path
from department.api.v1.department_view import customer_list_by_department_id, DepartmentView , DepartmentDetailView, reassigned_users_to_other_department


urlpatterns = [
    path('', DepartmentView.as_view()),
    path('<int:department_id>/', DepartmentDetailView.as_view()),
    path('<int:department_id>/customer/', customer_list_by_department_id),
    path('<int:id>/reassigned_users/', reassigned_users_to_other_department)
    ]