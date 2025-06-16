from django import forms
from employees.models import Employee_data

class OvertimeAssignForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee_data.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select employees to assign overtime"
    )

    def __init__(self, department, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employees'].queryset = Employee_data.objects.filter(department=department)





# leave_management/forms.py

from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
