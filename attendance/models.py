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
    is_late = models.BooleanField(default=False)




class ManualAttendanceRequest(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='manual_attendance_images/')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True) #Hr defined
    location_name = models.CharField(max_length=100, blank=True, null=True)  # remote employee location
    latitude = models.FloatField()
    longitude = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Manual Attendance Request by {self.employee} on {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"
    



from django.db import models

class AttendanceSettings(models.Model):
    shift_start = models.TimeField(default="09:00")
    shift_end = models.TimeField(default="17:00")
    working_days = models.IntegerField(default=30)
    hours_per_day = models.DecimalField(default=8.0, max_digits=5, decimal_places=2)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attendance Settings (updated {self.updated_at.date()})"

    class Meta:
        verbose_name_plural = "Attendance Settings"
