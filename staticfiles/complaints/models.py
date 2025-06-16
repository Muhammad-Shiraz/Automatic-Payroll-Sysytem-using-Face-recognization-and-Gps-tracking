from django.db import models
from employees.models import Employee_data

class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('Harassment', 'Harassment'),
        ('Workload Issue', 'Workload Issue'),
        ('Salary Dispute', 'Salary Dispute'),
        ('Unfair Treatment', 'Unfair Treatment'),
        ('Workplace Safety', 'Workplace Safety'),
        ('Discrimination', 'Discrimination'),
        ('Other', 'Other'),
    ]

    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_TYPES)
    details = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.complaint_type}"



from django.db import models
from employees.models import Employee_data

class EmployeeFeedback(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    suggestion = models.CharField(max_length=255)
    feedback = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.employee.name} - {self.rating}⭐ - {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"

