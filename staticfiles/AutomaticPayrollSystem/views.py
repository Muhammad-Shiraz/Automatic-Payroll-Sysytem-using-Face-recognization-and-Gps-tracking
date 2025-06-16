from django.shortcuts import render,redirect
from employees.models import Employee_data
from attendance.models import Attendance , Location
from django.db.models import Sum  # Import Sum
from decimal import Decimal
from datetime import date
from django.contrib.auth.decorators import login_required

from payroll.models import Payroll,DailyPayroll
from calendar import monthrange

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from calendar import monthrange
from django.db.models import Sum
from decimal import Decimal

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name="HR").exists():
        return redirect('hr_dashboard')
    elif user.groups.filter(name="Employee").exists():
        return redirect('emp_dashboard')  # employee dashboard url name
    else:
        return redirect('login')


@login_required
def hr_dashboard(request):
    user = request.user
    if not user.groups.filter(name="HR").exists():
        return redirect('login')  # or some unauthorized page

    template = "index.html"  # Your HR dashboard template

    today = date.today()
    first_day = date(today.year, today.month, 1)
    last_day = date(today.year, today.month, monthrange(today.year, today.month)[1])

    employees = Employee_data.objects.all()
    total_employees = employees.count()

    employee_data = []
    for emp in employees:
        payroll = Payroll.objects.filter(
            employee=emp.employee_id,
            month__year=today.year,
            month__month=today.month
        ).first()

        present_days = Attendance.objects.filter(
            employee=emp,
            status="Present",
            date__range=(first_day, last_day)
        ).count()

        overtime_pay = DailyPayroll.objects.filter(
            employee=emp.employee_id,
            date__range=(first_day, last_day)
        ).aggregate(total_overtime=Sum("overtimepay"))["total_overtime"] or Decimal("0.00")

        employee_data.append({
            "employee_id": emp.employee_id,
            "employee_images": emp.employee_images,
            "name": emp.name,
            "department": emp.department,
            "present_days": present_days,
            "monthly_salary": payroll.total_salary if payroll else Decimal("0.00"),
            "overtime_pay": overtime_pay,
        })

    total_payroll = Payroll.objects.filter(
        month__year=today.year,
        month__month=today.month
    ).aggregate(total=Sum("total_salary"))["total"] or Decimal("0.00")

    attendance_today = Attendance.objects.filter(date=today)
    total_present = attendance_today.filter(status="Present").count()
    total_absent = attendance_today.filter(status="Absent").count()

    context = {
        "employee_data": employee_data,
        "total_employees": total_employees,
        "total_payroll": total_payroll,
        "total_present": total_present,
        "total_absent": total_absent,
        "user": user,
    }

    return render(request, template, context)
















@login_required
def settings(request):
    return render(request, 'settings.html')

@login_required
def Manualoverride(request):
    return render(request, 'Manual-override.html')

@login_required
def live_camera_redirect(request):
    return render(request, "face.html")  # Now it loads the correct page

@login_required
def dashboard_redirect(request):
    return redirect("home")
