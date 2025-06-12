from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import Attendance
from payroll.models import DailyPayroll, Payroll
from django.utils.timezone import now, localdate
from payroll.views import get_daily_payroll_data
from decimal import Decimal
from employees.models import Employee_data
from performance.views import calculate_employee_performance  # triggers bonus logic

@receiver(post_save, sender=Attendance)
def create_or_update_payroll(sender, instance, **kwargs):
    if not instance.time_out:
        return  # Ignore incomplete attendance

    try:
        print("🔁 Refreshing DailyPayroll data...")
        get_daily_payroll_data()
    except Exception as e:
        print("❌ Failed to refresh DailyPayroll:", str(e))
        return

    today = localdate()
    payroll_month = today.replace(day=1)

    # Step 1: Update performance and bonus once per month (this function handles bonus saving)
    try:
        print(f"📈 Calculating performance for {instance.employee.name}")
        calculate_employee_performance(instance.employee, payroll_month)
    except Exception as e:
        print("❌ Performance calculation failed:", str(e))

    # Step 2: Get this employee's daily entries for the month
    daily_entries = DailyPayroll.objects.filter(
        employee=instance.employee,
        date__month=today.month,
        date__year=today.year
    )

    if not daily_entries.exists():
        print(f"⚠️ No DailyPayroll found for {instance.employee}")
        return

    total_hours = sum(entry.hours_worked for entry in daily_entries)
    total_salary = sum(entry.daily_salary for entry in daily_entries)
    total_overtime = sum(entry.overtime for entry in daily_entries)

    # Step 3: Get or create Payroll and include performance_bonus in total_salary
    payroll, created = Payroll.objects.get_or_create(
        employee=instance.employee,
        month=payroll_month,
        defaults={
            'basic_salary': instance.employee.salary,
            'total_hours': total_hours,
            'overtime': total_overtime,
            'status': 'pending'
        }
    )

    performance_bonus = payroll.performance_bonus if payroll.performance_bonus else Decimal(0)

    # Step 4: Update the total salary including bonus (only once per month)
    payroll.total_hours = total_hours
    payroll.overtime = total_overtime
    payroll.total_salary = round(total_salary + performance_bonus, 2)
    payroll.save()

    print(f"✅ Payroll updated for {instance.employee.name}")
