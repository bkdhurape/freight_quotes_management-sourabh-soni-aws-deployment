from department.models.department import Department
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueTogetherValidator


class DepartmentSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'status', 'name', 'type', 'company']
        read_only_fields = ['id']

 
class DepartmentValidateSerializer(serializers.ModelSerializer): 

    """Add and Update department seriallizer """
    
    class Meta:
        model = Department
        fields = ['name', 'company']
        read_only_fields = ['id']

        validators = [UniqueTogetherValidator(queryset=Department.objects.all(), fields=[
                                              'company', 'name'], message='The department name already exists for this company')]

       
