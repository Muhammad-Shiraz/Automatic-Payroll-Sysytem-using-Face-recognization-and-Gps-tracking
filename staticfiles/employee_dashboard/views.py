from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ManualAttendanceForm
from attendance.models import Attendance
from payroll.models import DailyPayroll
from performance.models import PerformanceKPI
from datetime import date
from django.db.models import Sum
from datetime import date

@login_required
def employee_dashboard(request):
    if request.user.groups.filter(name="Employee").exists():
        try:
            employee = request.user.employee_data

            # Get current month date range
            today = date.today()
            start_of_month = today.replace(day=1)
            if today.month == 12:
                end_of_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                end_of_month = today.replace(month=today.month + 1, day=1)

            # Attendance data
            attendance = Attendance.objects.filter(employee=employee, date__gte=start_of_month, date__lt=end_of_month).order_by('-date')
            present_days = Attendance.objects.filter(
                employee=employee,
                date__gte=start_of_month, 
                date__lt=end_of_month,
                status="Present"
            ).count()

            

            # Calculate salary and overtime from DailyPayroll
            daily_data = DailyPayroll.objects.filter(
                employee=employee,
                date__gte=start_of_month,
                date__lt=end_of_month).aggregate(
                total_salary=Sum('daily_salary'),
                total_overtime=Sum('overtimepay')
            )

            performancekpi = PerformanceKPI.objects.filter(employee=employee, month__year=today.year, month__month=today.month).first()

            # Defaults if no data
            monthly_salary = daily_data['total_salary'] or 0
            monthly_overtime = daily_data['total_overtime'] or 0
            total_monthly_pay = round(monthly_salary + monthly_overtime, 2)


            # Add this below performancekpi line
            if performancekpi:
                kpi_scores = {
                    'Attendance_Rate': performancekpi.attendance_rate,
                    'Punctuality_Score': performancekpi.punctuality_score,
                    'Task_Completion_Rate': performancekpi.task_completion_rate,
                    
                }
            else:
                kpi_scores = {}

            # Inside employee_dashboard view after calculating present_days

            auto_attendance_count = Attendance.objects.filter(
                employee=employee,
                date__gte=start_of_month,
                date__lt=end_of_month,
                method='Auto'
            ).count()

            manual_attendance_count = Attendance.objects.filter(
                employee=employee,
                date__gte=start_of_month,
                date__lt=end_of_month,
                method='Manual'
            ).count()

            if Attendance.objects.filter(employee=employee, date__gte=start_of_month, date__lt=end_of_month).exists():
                attendance_progress = {
                    'auto_attendance': auto_attendance_count,
                    'manual_attendance': manual_attendance_count,
                    'Leave_Days': performancekpi.leave_days
                    
                }
            # print(attendance)
            # print(attendance.method)

            # Leave Balances
            leave_balance = {
                'casual': 0,
                'sick': 5,
                'earned':2,
            }

            # Pending tasks
            pending_tasks = TaskAssignment.objects.filter(
                employee=employee,
                is_completed=False
            ).count()

            # Latest payroll
            latest_payroll_record = Payroll.objects.filter(
                employee=employee
            ).order_by('-month').first()

            latest_payroll = None
            if latest_payroll_record:
                start_of_month = latest_payroll_record.month.replace(day=1)
                if latest_payroll_record.month.month == 12:
                    end_of_month = latest_payroll_record.month.replace(year=latest_payroll_record.month.year + 1, month=1, day=1)
                else:
                    end_of_month = latest_payroll_record.month.replace(month=latest_payroll_record.month.month + 1, day=1)

                monthly_overtime = DailyPayroll.objects.filter(
                    employee=employee,
                    date__gte=start_of_month,
                    date__lt=end_of_month
                ).aggregate(total=Sum('overtimepay'))['total'] or 0

                latest_payroll = {
                    'month': latest_payroll_record.month,
                    'total_salary': round(float(latest_payroll_record.total_salary), 2),
                    'bonus': round(float(latest_payroll_record.bonus), 2),
                    'performance_bonus': round(float(latest_payroll_record.performance_bonus), 2),
                    'overtime': round(monthly_overtime, 2),
                }
                    


        except Exception as e:
            print("Error getting employee data or payroll:", e)
            return redirect('unauthorized')

        content = {
            'employee': employee,
            'attendance': attendance,
            'present_days': present_days,
            'monthly_salary': round(monthly_salary, 2),
            'monthly_overtime': round(monthly_overtime, 2),
            'total_monthly_pay': total_monthly_pay,
            'performancekpi': performancekpi,
            'kpi_scores': kpi_scores,
            'attendance_progress': attendance_progress,
            'leave_balance': leave_balance,
            'pending_tasks': pending_tasks,
            'latest_payroll': latest_payroll,
        }
        return render(request, 'emp_dashboard.html', content)
    else:
        return redirect('unauthorized')




from geopy.distance import geodesic
from attendance.models import ManualAttendanceRequest, Location
from employees.models import Employee_data
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required
import base64
from django.core.files.base import ContentFile

@login_required
def submit_manual_attendance(request):
    employee = get_object_or_404(Employee_data, user=request.user)

    if request.method == 'POST':

        image_data = request.POST.get('image_data')
        if not image_data:
            messages.error(request, "Image capture failed.")
            return redirect('submit_manual_attendance')

        # print(image_data)
        format, imgstr = image_data.split(';base64,')  # format ~= data:image/png
        # print(format)
        ext = format.split('/')[-1]
        # print(ext)
        image_file = ContentFile(base64.b64decode(imgstr), name=f"{employee.name}_{date.today()}.{ext}")

        lat = float(request.POST.get('latitude', 0))
        lon = float(request.POST.get('longitude', 0))

        if not image_file or lat == 0.0 or lon == 0.0:
            messages.error(request, "Image and location are required.")
            return redirect('submit_manual_attendance')

        matched_location = None
        closest_distance = float('inf')

        for loc in Location.objects.all():
            try:
                loc_lat, loc_lon = map(float, loc.gps_coordinates.split(','))
                distance = geodesic((lat, lon), (loc_lat, loc_lon)).meters
                if distance < closest_distance:
                    closest_distance = distance
                    matched_location = loc
            except:
                continue

        if closest_distance >= 100 and not employee.remote_status:
            messages.error(request, "You are outside the office and not allowed remote work. Request auto-rejected.")
            return redirect('submit_manual_attendance')

        # ✅ Corrected logic for location + location_name
        ManualAttendanceRequest.objects.create(
            employee=employee,
            image=image_file,
            latitude=lat,
            longitude=lon,
            location=matched_location if closest_distance < 100 else None,
            location_name=None if closest_distance < 100 else f"Remote - {employee.name}"
        )

        messages.success(request, "Manual attendance request submitted for HR review.")
        return redirect('submit_manual_attendance')

    return render(request, 'manual_attendance_form.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from datetime import date, timedelta
from performance.models import EmployeePerformance, PerformanceKPI, HRFeedback, PerformanceBonusRule
from employees.models import Employee_data

@login_required
def employee_performance_dashboard(request):
    user = request.user
    try:
        employee = Employee_data.objects.get(user=user)
    except Employee_data.DoesNotExist:
        return render(request, 'performance/no_employee.html')

    current_month = date.today().replace(day=1)

    # Get current month performance
    performance = EmployeePerformance.objects.filter(employee=employee, month=current_month).first()
    if performance:
        score = performance.overall_score
        grade = performance.grade
        kpi = performance.kpi
        feedback = performance.hr_feedback
    else:
        score = 0
        grade = None
        kpi = None
        feedback = None

    # Get past 6 months (oldest to newest)
    past_months = [current_month - timedelta(days=30 * i) for i in range(6)][::-1]

    performances = EmployeePerformance.objects.filter(
        employee=employee, month__in=past_months
    ).select_related('kpi').order_by('month')

    months = [perf.month.strftime('%b') for perf in performances]
    scores = [perf.overall_score for perf in performances]

    # KPI trends for stacked area chart
    attendance_rates = [perf.kpi.attendance_rate if perf.kpi else 0 for perf in performances]
    punctuality_scores = [perf.kpi.punctuality_score if perf.kpi else 0 for perf in performances]
    task_completion_rates = [perf.kpi.task_completion_rate if perf.kpi else 0 for perf in performances]
    # leave_days = [perf.kpi.leave_penalty if perf.kpi else 0 for perf in performances]

    # Bonus eligibility (1 or 0 per month)
    bonus_rule = PerformanceBonusRule.objects.first()
    bonus_threshold = bonus_rule.min_score_threshold if bonus_rule else 0
    bonus_eligibility = [
        1 if perf.overall_score >= bonus_threshold else 0 for perf in performances
    ]

    # Current month KPI breakdown
    if kpi:
        kpi_labels = ['Attendance Rate', 'Punctuality Score', 'Task Completion Rate']
        kpi_scores = [kpi.attendance_rate, kpi.punctuality_score, kpi.task_completion_rate]
    else:
        kpi_labels = []
        kpi_scores = []

    # HR feedback
    rating = feedback.rating if feedback else 0
    feedback_text = feedback.comments if feedback else "No feedback yet"

    # Department average
    department_employees = Employee_data.objects.filter(department=employee.department)
    dept_avg = EmployeePerformance.objects.filter(
        employee__in=department_employees, month=current_month
    ).aggregate(avg_score=Avg('overall_score'))['avg_score'] or 0

    # Bonus calculation
    bonus = bonus_rule.bonus_amount if bonus_rule and score >= bonus_threshold else 0
    remaining_score = 100 - score

    context = {
        "employee": employee,
        "score": score,
        "remaining_score": remaining_score,
        "grade": grade,
        "months": months,
        "scores": scores,
        "kpi_labels": kpi_labels,
        "kpi_scores": kpi_scores,
        "rating": rating,
        "feedback_text": feedback_text,
        "dept_avg": int(dept_avg),
        "bonus": bonus,

        # New chart data
        "attendance_rates": attendance_rates,
        "punctuality_scores": punctuality_scores,
        "task_completion_rates": task_completion_rates,
        # "leave_days": leave_days,
        "bonus_eligibility": bonus_eligibility,
    }

    return render(request, "emp_performance.html", context)





from performance.models import TaskAssignment
@login_required
def employee_task(request):
    employee = request.user.employee_data
    task = TaskAssignment.objects.filter(employee=employee).order_by('-assigned_date')
    return render(request, 'employee_task.html', {'task': task})

def emp_attendance(request):
    employee = request.user.employee_data
    attendance = Attendance.objects.filter(employee=employee).order_by('-date')
    return render(request, 'emp_attendance.html', {'attendance': attendance})
    



from attendance.models import Attendance
from django.shortcuts import render
from collections import defaultdict

def attendance_analytics(request):
    employee = request.user.employee_data
    attendance = Attendance.objects.filter(employee=employee)

    monthly_data = defaultdict(lambda: {'Present': 0, 'Absent': 0, 'Late': 0})

    for att in attendance:
        month = att.date.strftime('%B')
        if att.status == 'Present':
            monthly_data[month]['Present'] += 1
            if att.is_late:
                monthly_data[month]['Late'] += 1
        else:
            monthly_data[month]['Absent'] += 1

    labels = list(monthly_data.keys())
    present_data = [monthly_data[month]['Present'] for month in labels]
    absent_data = [monthly_data[month]['Absent'] for month in labels]
    late_data = [monthly_data[month]['Late'] for month in labels]

    success_month = max(monthly_data.items(), key=lambda x: x[1]['Present'])[0] if monthly_data else 'N/A'

    total_present = sum(present_data)
    total_absent = sum(absent_data)
    total_late = sum(late_data)

    context = {
        'labels': labels,
        'present_data': present_data,
        'absent_data': absent_data,
        'late_data': late_data,
        'success_month': success_month,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
    }

    return render(request, 'emp_attendance_analytics.html', context)



from django.shortcuts import render
from payroll.models import Payroll, DailyPayroll
from datetime import datetime
from django.db.models import Sum


from django.shortcuts import render
from django.db.models import Sum
import json

def employee_payroll_view(request):
    employee = request.user.employee_data
    payroll_records = Payroll.objects.filter(employee=employee).order_by('-month')

    combined_data = []

    labels = []
    salary_data = []
    bonus_data = []
    performance_bonus_data = []
    overtime_data = []

    for record in payroll_records:
        # Month start and end
        start_of_month = record.month.replace(day=1)
        if record.month.month == 12:
            end_of_month = record.month.replace(year=record.month.year + 1, month=1, day=1)
        else:
            end_of_month = record.month.replace(month=record.month.month + 1, day=1)

        monthly_overtime = DailyPayroll.objects.filter(
            employee=employee,
            date__gte=start_of_month,
            date__lt=end_of_month
        ).aggregate(total=Sum('overtimepay'))['total'] or 0

        labels.append(record.month.strftime("%b %Y"))
        salary_data.append(float(record.total_salary))
        bonus_data.append(float(record.bonus))
        performance_bonus_data.append(float(record.performance_bonus))
        overtime_data.append(round(float(monthly_overtime), 2))

        combined_data.append({
            "record": record,
            "month": record.month.strftime("%B %Y"),
            "basic_salary": float(record.basic_salary),
            "bonus": float(record.bonus),
            "performance_bonus": float(record.performance_bonus),
            "total_salary": float(record.total_salary),
            "overtime": round(float(monthly_overtime), 2),
            "status": record.status,
        })

    context = {
        "combined_data": combined_data,
        "labels": json.dumps(labels),
        "salary_data": json.dumps(salary_data),
        "bonus_data": json.dumps(bonus_data),
        "performance_bonus": json.dumps(performance_bonus_data),
        "overtime_data": json.dumps(overtime_data),
    }

    return render(request, "emp_payroll.html", context)




def daily_payroll_view(request, month):
    employee = request.user.employee_data
    year, month_num = map(int, month.split('-'))

    daily_records = DailyPayroll.objects.filter(
        employee=employee,
        date__year=year,
        date__month=month_num
    ).order_by('date')

    return render(request, 'daily_payroll.html', {
        'daily_records': daily_records,
        'month_label': datetime(year, month_num, 1).strftime('%B %Y')
    })


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_payroll_slip(request):
    try:
        employee = request.user.employee_data
        payroll = Payroll.objects.filter(employee=employee).latest('month')

        html_string = render_to_string("slip_template.html", {'employee': employee, 'payroll': payroll})
        output_path = os.path.join(settings.MEDIA_ROOT, f"payroll_slips/{employee.employee_id}_slip.pdf")
        print("PDF will be saved to:", output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        HTML(string=html_string).write_pdf(output_path)

        # Send email
        email = EmailMessage(
            subject="Your Monthly Payroll Slip",
            body=render_to_string("email_template.html", {"employee": employee}),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[employee.email]
        )
        email.content_subtype = 'html'
        email.attach_file(output_path)
        email.send()

        return JsonResponse({'pdf_url': settings.MEDIA_URL + f"payroll_slips/{employee.employee_id}_slip.pdf"})

    except Exception as e:
        # Log the error if you have logging
        return JsonResponse({'error': str(e)}, status=500)




@login_required
def payroll_slip(request):
    return render(request, "payroll_slip.html")




# employee_dashboard/views.py

from leave_management.forms import LeaveRequestForm

@login_required
def emp_leave_request(request):
    employee = Employee_data.objects.get(user=request.user)

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            messages.success(request, "Your leave request has been submitted!")
            return redirect('emp_dashboard')  # adjust this
    else:
        form = LeaveRequestForm()

    return render(request, 'emp_leave_request.html', {'form': form})


from django.db.models import Prefetch
from leave_management.models import LeaveRequest,OvertimeInvitation

@login_required
def my_leave_requests(request):
    employee = request.user.employee_data  # Get logged in employee

    leaves = LeaveRequest.objects.filter(employee=employee).select_related(
        'leave_type', 'assigned_employee'
    ).prefetch_related(
        Prefetch(
            'overtimeinvitation_set',
            queryset=OvertimeInvitation.objects.select_related('employee'),
            to_attr='overtime_invites'
        )
    ).order_by('-applied_on')

    return render(request, 'my_leave_requests.html', {
        'leaves': leaves
    })





from django.shortcuts import render, redirect
from complaints.models import Complaint
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render, redirect
from complaints.models import Complaint  # Your Complaint model
from employees.models import Employee_data
from django.contrib.auth.decorators import login_required

@login_required
def submit_complaint(request):
    employee = request.user.employee_data  # Assumes employee is linked to user

    if request.method == "POST":
        complaint_type = request.POST.get("complaint_type")
        details = request.POST.get("details")

        # Save the complaint
        Complaint.objects.create(
            employee=employee,
            complaint_type=complaint_type,
            details=details
        )

        messages.success(request, "✅ Your complaint has been submitted successfully.")

    return render(request, "submit_complaint.html")




# employee_dashboard/views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from complaints.models import EmployeeFeedback  # or adjust import path

@login_required
def employee_feedback_view(request):
    employee = request.user.employee_data

    if request.method == 'POST':
        rating = request.POST.get('rating')
        suggestion = request.POST.get('suggestion')
        feedback = request.POST.get('feedback')

        if rating and suggestion and feedback:
            EmployeeFeedback.objects.create(
                employee=employee,
                rating=rating,
                suggestion=suggestion,
                feedback=feedback
            )
            messages.success(request, "✅ Thank you for your feedback!")
            return redirect('employee_feedback')

    return render(request, 'employee_feedback.html')



@login_required
def update_employee_profile(request):
    employee = request.user.employee_data

    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        image = request.FILES.get('employee_images')

        if phone:
            employee.phone = phone
        if address:
            employee.address = address
        if image:
            employee.employee_images = image

        employee.save()
        return redirect('emp_dashboard')  # Update with your actual dashboard URL name

    return redirect('emp_dashboard')


