from django.contrib import admin

# Register your models here.
from attendance.models import ManualAttendanceRequest

admin.site.register(ManualAttendanceRequest)