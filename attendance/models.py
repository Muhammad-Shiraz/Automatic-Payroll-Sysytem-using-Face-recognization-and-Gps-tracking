# attendance/models.py
from django.db import models
from datetime import date
from employees.models import Employee_data

class Location(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Main Office"
    gps_coordinates = models.CharField(max_length=255)  # "lat,lon"

    def __str__(self):
        return f"{self.name} ({self.gps_coordinates})"
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    employee = models.ForeignKey(Employee_data, to_field='employee_id', on_delete=models.CASCADE)
    date = models.DateField(default=date.today) 
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    method = models.CharField(max_length=10, choices=[('Auto', 'Auto'), ('Manual', 'Manual')])
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES , default='Absent',blank=False)