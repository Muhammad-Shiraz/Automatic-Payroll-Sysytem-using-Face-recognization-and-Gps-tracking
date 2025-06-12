# === ✅ Create this in payroll/utils.py ===

from datetime import datetime, date
from decimal import Decimal
from employees.models import Employee_data
from attendance.models import Attendance, AttendanceSettings
from payroll.models import Payroll, DailyPayroll, PayrollSettings

from django.db.models import Sum

def get_daily_payroll_data():
    employees = Employee_data.objects.all()
    payrollSettings = PayrollSettings.objects.first()
    attendanceSettings = AttendanceSettings.objects.first()

    shift_hours = Decimal(attendanceSettings.hours_per_day) if attendanceSettings else Decimal(8)
    working_days = int(attendanceSettings.working_days) if attendanceSettings else 22
    overtime_percentage = Decimal(payrollSettings.overtime_rate) if payrollSettings else Decimal(100.0)

    payroll_data = []

    for employee in employees:
        basic_salary = Decimal(employee.salary)
        attendance_records = Attendance.objects.filter(employee=employee, date=date.today())

        total_hours = Decimal(0)
        total_overtime_hours = Decimal(0)
        current_month = date.today().replace(day=1)

        for record in attendance_records:
            if record.time_in and record.time_out:
                dt_in = datetime.combine(record.date, record.time_in)
                dt_out = datetime.combine(record.date, record.time_out)
                worked_hours = Decimal((dt_out - dt_in).total_seconds()) / Decimal(3600)
                total_hours += worked_hours
                if worked_hours > shift_hours:
                    total_overtime_hours += (worked_hours - shift_hours)

        monthly_work_hours = Decimal(working_days) * shift_hours
        hourly_rate = basic_salary / monthly_work_hours
        bonus = basic_salary * Decimal(0)

        regular_hours = total_hours - total_overtime_hours
        regular_pay = hourly_rate * regular_hours
        overtime_bonus = hourly_rate * total_overtime_hours * (overtime_percentage / 100)
        overtime_pay = (hourly_rate * total_overtime_hours) + overtime_bonus
        print(overtime_pay)
        print(overtime_bonus)
        print(regular_hours, regular_pay, overtime_bonus,overtime_pay)
        daily_salary = regular_pay + (hourly_rate * total_overtime_hours) + overtime_bonus
        print(daily_salary)
        print(f"Employee: {employee.name}, Basic Salary: {basic_salary}")
        print(f"Total Hours: {total_hours}, Overtime Hours: {total_overtime_hours}")
        print(f"Hourly Rate: {hourly_rate}, Daily Salary: {daily_salary}")
        print(f"Overtime Pay: {overtime_pay}, Bonus: {bonus}")


        DailyPayroll.objects.update_or_create(
            employee=employee,
            date=date.today(),
            defaults={
                'hours_worked': round(total_hours, 2),
                'hourly_rate': round(hourly_rate, 2),
                'daily_salary': round(daily_salary, 2),
                'overtime': round(total_overtime_hours, 2),
                'overtimepay': round(overtime_pay, 2),
            }
        )

        Payroll.objects.update_or_create(
            employee=employee,
            month=current_month,
            defaults={
                'basic_salary': basic_salary,
                'bonus': bonus,
                'status': 'pending'
                # 'total_hours': round(total_hours, 2),
                # 'overtime': round(total_overtime_hours, 2),  # Store overtime separately
                # 'total_salary': round(daily_salary + overtime_pay + bonus, 2),  # Total salary for the day
            }
        )

        payroll_data.append({
            'employee_id': employee.employee_id,
            'name': employee.name,
            'department': employee.department,
            'hours_worked': round(total_hours, 2),
            'hourly_rate': round(hourly_rate, 2),
            'total_pay': round(daily_salary, 2),
            'status': employee.active_status,
            'basic_salary': round(basic_salary, 2),
            'overtime': round(overtime_pay, 2),
            'bonus': round(bonus, 2),
        })

    return payroll_data
