import os
from django.db import models
from django.contrib.auth.models import User

def employee_image_path(instance, filename):
    """
    Save images with the employee's auto-generated ID as the filename.
    (The file will be stored as "<employee_id>.<extension>" in the "employee_images/" folder.)
    """
    ext = filename.split('.')[-1]
    filename = f"{instance.employee_id}.{ext}"
    return os.path.join('employee_images/', filename) # Save in 'employee_images/' directory

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_data', null=True, blank=True)
    employee_id = models.AutoField(primary_key=True)  # Auto-increment ID
    is_hr = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married')], null=True)

    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postalCode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    shift = models.CharField(max_length=50, choices=[('Morning', 'Morning'), ('Evening', 'Evening'), ('Night', 'Night')], null=True)
    employmentType = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract')], null=True)
    active_status = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    joining_date = models.DateField(null=True, blank=True)
    remote_status = models.BooleanField(default=False)  # True if the employee works remotely
    bankAccount = models.CharField(max_length=30, null=True, blank=True)
    bankName = models.CharField(max_length=100, null=True, blank=True)

    emergencyContactName = models.CharField(max_length=100, null=True, blank=True)
    emergencyContactrelationship = models.CharField(max_length=50, null=True, blank=True)
    emergencyContactPhone = models.CharField(max_length=15, null=True, blank=True)

    employee_images = models.ImageField(upload_to=employee_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"  # Display ID instead of Name
