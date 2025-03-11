from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, date
from attendance.models import Attendance
from payroll.models import Payroll
from employees.models import Employee_data




def payroll_dashboard(request):
    # Retrieve all employees from Employee_data (which should include a salary field)
    employees = Employee_data.objects.all()

    payroll_data = []
    for employee in employees:
        # Retrieve the employee's basic salary from the Employee_data model.
        # Make sure your Employee_data model has a salary field (or basic_salary field)
        basic_salary = employee.salary  # Replace with your actual field name, e.g., employee.basic_salary
        
        # Fetch attendance records for today (or adjust the date range as needed)
        attendance_records = Attendance.objects.filter(employee=employee, date=date.today())
        
        total_hours = 0
        for record in attendance_records:
            if record.time_in and record.time_out:
                # Combine date and time to calculate the difference
                dt_in = datetime.combine(record.date, record.time_in)
                dt_out = datetime.combine(record.date, record.time_out)
                total_hours += (dt_out - dt_in).total_seconds() / 3600

        # Calculate hourly rate based on an assumed monthly working hours (e.g., 160 hours per month)
        hourly_rate = float(basic_salary)
        
        # Total pay is calculated based on the actual hours worked
        total_pay = hourly_rate * total_hours

        payroll_data.append({
            'employee_id': employee.employee_id,  # or employee.id if not using a separate field
            'name': employee.name,
            'hours_worked': round(total_hours, 2),
            'hourly_rate': round(hourly_rate, 2),
            'total_pay': round(total_pay, 2),
        })

    return render(request, 'payroll.html', {'employees': payroll_data})


# from django.utils.timezone import now
# from attendance.models import Attendance
# from employees.models import Employee_data

# def update_daily_payroll():
#     today = date.today()
#     employees = Employee_data.objects.all()

#     for employee in employees:
#         attendance = Attendance.objects.filter(employee=employee, date=today).first()
        
#         if attendance and attendance.time_in and attendance.time_out:
#             hours_worked = (attendance.time_out.hour + attendance.time_out.minute / 60) - \
#                            (attendance.time_in.hour + attendance.time_in.minute / 60)
#         else:
#             hours_worked = 0  # If absent, hours worked is 0

#         payroll, created = DailyPayroll.objects.get_or_create(employee=employee, date=today)
#         payroll.hours_worked = hours_worked
#         payroll.hourly_rate = employee.salary / 160  # Assuming 160 hours per month
#         payroll.save()
