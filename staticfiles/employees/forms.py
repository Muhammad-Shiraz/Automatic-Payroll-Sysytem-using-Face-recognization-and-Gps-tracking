from django import forms
from .models import Department, Designation

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']  # Assuming your Department model has a `name` field

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name']  # Assuming your Designation model has a `name` field
