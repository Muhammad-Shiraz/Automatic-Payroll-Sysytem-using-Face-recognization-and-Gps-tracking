from django.shortcuts import render,redirect
from employees.models import Employee_data
from attendance.models import Attendance , Location
from django.db.models import Sum  # Import Sum
from decimal import Decimal
from datetime import date

# def homePage(request):
#     employees = Employee_data.objects.all()
#     attendance = Attendance.objects.all()
#     total_employees = employees.count() 
#     employees_salary = employees.aggregate(total_salary=Sum('salary'))['total_salary']
#     attendance_queryset = Attendance.objects.filter(date=date.today())
#     total_present = attendance_queryset.filter(status='Present').count()
#     totalabsent= attendance_queryset.filter(status='Absent').count()

#     # If no employees exist, avoid 'NoneType' error by setting default value to Decimal(0)
#     if employees_salary is None:
#         employees_salary = Decimal(0)

#     return render(request,'index.html', {'employees': employees, 'total_employees': total_employees, 'employees_salary': employees_salary, 'total_present': total_present})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from decimal import Decimal
from employees.models import Employee_data
from attendance.models import Attendance

@login_required
def homePage(request):
    user = request.user  # Get logged-in user

    # Determine the dashboard template based on user group
    if user.groups.filter(name="HR").exists():
        template = "index.html"  # HR Dashboard
    elif user.groups.filter(name="Employee").exists():
        template = "emp_dashboard.html"  # Employee Dashboard
    else:
        return redirect("login")  # Redirect if no group is assigned

    # Employee and Attendance Data
    employees = Employee_data.objects.all()
    attendance_queryset = Attendance.objects.filter(date=date.today())

    total_employees = employees.count()
    total_present = attendance_queryset.filter(status="Present").count()
    total_absent = attendance_queryset.filter(status="Absent").count()
    
    employees_salary = employees.aggregate(total_salary=Sum("salary"))["total_salary"] or Decimal(0)

    return render(request, template, {
        "employees": employees,
        "total_employees": total_employees,
        "employees_salary": employees_salary,
        "total_present": total_present,
        "total_absent": total_absent,  # Added absent count
    })

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

