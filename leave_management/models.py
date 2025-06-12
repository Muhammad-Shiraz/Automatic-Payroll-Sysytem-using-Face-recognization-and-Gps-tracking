from django.db import models
from django.utils import timezone
from employees.models import Employee_data

class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    emails_sent = models.BooleanField(default=False)
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_on = models.DateTimeField(null=True, blank=True)
    assigned_employee = models.ForeignKey(
    Employee_data,
    null=True, blank=True,
    related_name='assigned_leaves',
    on_delete=models.SET_NULL
    )


    def approve(self):
        self.status = 'Approved'
        self.reviewed_on = timezone.now()
        self.save()
        return self.employee.department

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type.name} ({self.status})"



class OvertimeInvitation(models.Model):
    leave = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    responded_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - Invitation for {self.leave}"
