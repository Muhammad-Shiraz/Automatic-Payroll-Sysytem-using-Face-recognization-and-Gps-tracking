from django.db import models
from employees.models import Employee_data
from django.utils import timezone

# 1. Performance Grade Mapping
class PerformanceGrade(models.Model):
    label = models.CharField(max_length=50)  # e.g., Excellent, Good, Average, Poor
    min_score = models.FloatField()
    max_score = models.FloatField()

    def __str__(self):
        return f"{self.label} ({self.min_score}-{self.max_score})"


# 2. Task (general task pool)
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 3. TaskAssignment
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    assigned_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.task.title} -> {self.employee.name}"


# 4. HR Feedback
class HRFeedback(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    feedback_date = models.DateField(default=timezone.now)
    rating = models.IntegerField(default=3)  # e.g., 1 to 5 stars
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"HR Feedback for {self.employee.name} on {self.feedback_date}"


# 6. Performance KPI (calculated metrics)
class PerformanceKPI(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    month = models.DateField(default=timezone.now)
    attendance_rate = models.FloatField(default=0)
    punctuality_score = models.FloatField(default=0)
    task_completion_rate = models.FloatField(default=0)
    leave_days = models.IntegerField(default=0)

    def __str__(self):
        return f"KPI for {self.employee.name} - {self.month.strftime('%B %Y')}"


# 7. EmployeePerformance (overall score)
class EmployeePerformance(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    month = models.DateField(default=timezone.now)
    kpi = models.OneToOneField(PerformanceKPI, on_delete=models.CASCADE)
    hr_feedback = models.ForeignKey(HRFeedback, on_delete=models.SET_NULL, null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    grade = models.ForeignKey(PerformanceGrade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Performance for {self.employee.name} - {self.month.strftime('%B %Y')}"


# 8. PerformanceHistory (optional backup/archive)
class PerformanceHistory(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    recorded_at = models.DateField(default=timezone.now)
    score = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History: {self.employee.name} on {self.recorded_at}"


# 9. TeamPerformance
class TeamPerformance(models.Model):
    department = models.CharField(max_length=100)
    month = models.DateField(default=timezone.now)
    average_score = models.FloatField(default=0)
    total_employees = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.department} - {self.month.strftime('%B %Y')}"
    


class PerformanceBonusRule(models.Model):
    min_score_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=90.00)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)

    def __str__(self):
        return f"If score >= {self.min_score_threshold}, give bonus {self.bonus_amount}"
