from django import forms
from attendance.models import ManualAttendanceRequest

class ManualAttendanceForm(forms.ModelForm):
    class Meta:
        model = ManualAttendanceRequest
        fields = ['location', 'image']


