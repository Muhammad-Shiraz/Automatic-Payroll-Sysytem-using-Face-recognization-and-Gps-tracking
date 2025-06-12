from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskAssignment
from .views import calculate_employee_performance
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import TaskAssignment

@receiver(post_save, sender=TaskAssignment)
def task_completed_handler(sender, instance, created, **kwargs):
    print("🚨 Signal triggered for task save")  # Put this at the top
    if instance.is_completed:
        print("✅ Signal triggered: Task marked as completed for employee", instance.employee.name)
        current_month = date.today().replace(day=1)
        calculate_employee_performance(instance.employee, current_month)

from .models import HRFeedback, PerformanceKPI
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=HRFeedback)
def update_kpi_on_feedback(sender, instance, created, **kwargs):
    if created:
        month_start = instance.feedback_date.replace(day=1)
        kpi, created = PerformanceKPI.objects.get_or_create(employee=instance.employee, month=month_start)
        # Example KPI update logic
        kpi.punctuality_score = (kpi.punctuality_score + float(instance.rating)) / 2
        kpi.save()
