from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from datetime import datetime, date
from payroll.models import Payroll, DailyPayroll, PayrollSettings
from employees.models import Employee_data
from attendance.models import Attendance , AttendanceSettings
from django.db.models import Sum
from .utils import get_daily_payroll_data

def payroll_dashboard(request):
    payroll_data = get_daily_payroll_data()
    total_salary_sum = Payroll.objects.all().aggregate(Sum('total_salary'))['total_salary__sum']
    bonus_sum = Payroll.objects.all().aggregate(Sum('bonus'))['bonus__sum']
    overtimepay_sum = DailyPayroll.objects.all().aggregate(Sum('overtimepay')).get('overtimepay__sum', 0)
    return render(request, 'payroll.html', {'employees_pay': payroll_data, 'total_salary_sum': total_salary_sum , 'bonus_sum': bonus_sum, 'overtimepay_sum': overtimepay_sum})





def employee_payroll_detail(request, employee_id):
    employee = get_object_or_404(Employee_data, employee_id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).order_by('month')
    daily_payroll = DailyPayroll.objects.filter(employee=employee).order_by('-date') 
    payroll_data2 = []

    for p in payrolls:
        # print(p.overtime, p.bonus)
        payroll_data2.append({
            'month': p.month.strftime("%B %Y"),
            'basic_salary': float(p.basic_salary),
            'total_salary': float(p.total_salary),
            'total_hours': float(p.total_hours),
            'start_date': p.start_date,
            'end_date': p.end_date,
            'status': p.status, # Assuming overtime is stored in the Payroll model
            'bonus': float(p.bonus),  # Assuming bonus is stored in the Payroll model
            'performance_bonus': float(p.performance_bonus) if p.performance_bonus else 0,
        })

    context = {
        'employee': employee,
        'payroll_data': payroll_data2,
        'daily_payroll': daily_payroll,
    }

    return render(request, 'employee_payroll.html', context)




from django.http import JsonResponse
from payroll.models import DailyPayroll
from decimal import Decimal

def payroll_chart_api(request):
    labels = []
    daily_salaries = []
    overtime_salaries = []

    # Fetch and group by date
    daily_payroll_entries = DailyPayroll.objects.all().order_by('date')

    for entry in daily_payroll_entries:
        date_str = entry.date.strftime('%b %d')

        if date_str not in labels:
            labels.append(date_str)
            daily_salaries.append(entry.daily_salary)
            overtime_salaries.append(entry.overtimepay)
        else:
            daily_salaries[labels.index(date_str)] += entry.daily_salary
            overtime_salaries[labels.index(date_str)] += entry.overtimepay

    return JsonResponse({
        'labels': labels,
        'daily_salaries': [float(val) for val in daily_salaries],
        'overtime_salaries': [float(val) for val in overtime_salaries],
    })







@csrf_exempt
def api_refresh_payroll_dashboard(request):
    data = get_daily_payroll_data()
    return JsonResponse({
        "status": "success",
        "message": "Payroll dashboard data refreshed.",
        "data": data
    })







# views.py
from django.shortcuts import render, redirect
from .models import PayrollSettings

def payroll_settings_view(request):
    payrollSettings, _ = PayrollSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        payrollSettings.overtime_rate = request.POST['overtime_rate']
        payrollSettings.save()
        get_daily_payroll_data()
        return redirect('payroll_settings')

    return render(request, 'payroll_setting.html', {'settings': payrollSettings})






def daily_salary_chart_api(request):
    data = (
        DailyPayroll.objects
        .order_by('date')
        .values('date')
        .annotate(total_salary=Sum('daily_salary'))
    )

    dates = [entry['date'].strftime('%Y-%m-%d') for entry in data]
    salaries = [float(entry['total_salary']) for entry in data]

    return JsonResponse({'dates': dates, 'salaries': salaries})




def payroll_chart_data(request):
    # Aggregating data from Payroll model
    payroll_data = Payroll.objects.aggregate(
        total_basic_salary=Sum('basic_salary'),
        total_bonus=Sum('bonus'),
        total_salary=Sum('total_salary')
    )

    # Aggregating data from DailyPayroll model for overtime
    daily_payroll_data = DailyPayroll.objects.aggregate(
        total_overtime_salary=Sum('overtimepay')
    )

    # Combine the data from both models
    combined_data = {
        'total_basic_salary': payroll_data['total_basic_salary'] or 0,
        'total_bonus': payroll_data['total_bonus'] or 0,
        'total_salary': payroll_data['total_salary'] or 0,
        'total_overtime_salary': daily_payroll_data['total_overtime_salary'] or 0
    }

    return JsonResponse(combined_data)