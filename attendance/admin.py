from django.contrib import admin

# Register your models here.
from .models import Location,Attendance

admin.site.register(Location)
admin.site.register(Attendance)