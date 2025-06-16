from django.shortcuts import render
from django.db.models import Avg
from datetime import date, timedelta
from decimal import Decimal
from employees.models import Employee_data
from .models import EmployeePerformance, PerformanceGrade, PerformanceKPI, HRFeedback, TaskAssignment
from attendance.models import Attendance , AttendanceSettings
from payroll.models import DailyPayroll

# from leave.models import LeaveRequest
from employees.models import Employee_data

# Utility: Get grade based on score
def get_grade_for_score(score):
    try:
        return PerformanceGrade.objects.get(min_score__lte=score, max_score__gte=score)
    except PerformanceGrade.DoesNotExist:
        return None

from datetime import timedelta

def get_working_days(start, end):
    settings = AttendanceSettings.objects.first()
    if settings and settings.working_days:
        return settings.working_days

    # fallback: auto calculate Mon–Fri working days
    delta = end - start
    working_days = 0
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        if day.weekday() < 5:
            working_days += 1
    return working_days


# Utility: Generate KPI for an employee for a given month
def generate_kpi(employee, month):
    start_date = month.replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    total_days = get_working_days(start_date, end_date)

    # Attendance
    present_days = Attendance.objects.filter(
        employee=employee,
        date__range=(start_date, end_date)
    ).count()
    print("😅Present Days:",present_days)
    attendance_rate = (present_days / total_days) * 100 if total_days else 0
    print("😅Attendance Rate:", attendance_rate)

    # Punctuality
    attendance_records = Attendance.objects.filter(
        employee=employee,
        date__range=(start_date, end_date)
    )

    present_days = attendance_records.count()

    # Punctuality (only if present at least one day)
    if present_days > 0:
        on_time_days = attendance_records.filter(is_late=False).count()
        punctuality_score = (on_time_days / present_days) * 100
    else:
        punctuality_score = 0.0


    # Task Completion
    assigned_tasks = TaskAssignment.objects.filter(
        employee=employee,
        assigned_date__range=(start_date, end_date)
    )
    completed_tasks = assigned_tasks.filter(is_completed=True)
    task_completion_rate = (completed_tasks.count() / assigned_tasks.count()) * 100 if assigned_tasks.exists() else 0
    print("😅Task Completion Rate:", task_completion_rate)
    # # Overtime: Fetch overtime hours from DailyPayroll
    # overtime_data = DailyPayroll.objects.filter(
    #     employee=employee,
    #     date__range=(start_date, end_date)
    # )
    # overtime_hours = sum(entry.overtime for entry in overtime_data)

    # Leave: Remove if you are not using LeaveRequest
    # leave_days = LeaveRequest.objects.filter(
    #     employee=employee,
    #     status='approved',
    #     start_date__lte=end_date,
    #     end_date__gte=start_date
    # ).count()

    kpi, created = PerformanceKPI.objects.update_or_create(
        employee=employee,
        month=start_date,
        defaults={
            'attendance_rate': attendance_rate,
            'punctuality_score': punctuality_score,
            'task_completion_rate': task_completion_rate,
            # 'leave_days': leave_days,  # Remove if you're not using LeaveRequest
        }
    )
    return kpi



# Utility: Calculate performance score and grade
from decimal import Decimal
from django.db.models import Avg

def calculate_employee_performance(employee, month):
    # print(f"🚀 Calculating performance for {employee} for {month}")
    kpi = generate_kpi(employee, month)
    print("🚀",kpi,"🚀 ")

    feedbacks = HRFeedback.objects.filter(
        employee=employee,
        feedback_date__month=month.month,
        feedback_date__year=month.year
    )
    avg_rating = feedbacks.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    # Define percentage-based weights (sum = 1.0)
    attendance_rate_weight = Decimal('0.25')
    punctuality_score_weight = Decimal('0.15')
    task_completion_rate_weight = Decimal('0.40')
    leave_penalty_weight = Decimal('0.10')
    rating_weight = Decimal('0.10')

    # Convert to Decimal
    attendance_rate = Decimal(kpi.attendance_rate)
    punctuality_score = Decimal(kpi.punctuality_score)
    task_completion_rate = Decimal(kpi.task_completion_rate)
    leave_days = Decimal(kpi.leave_days)

    # Normalize HR feedback (rating out of 5 to percentage)
    feedback_score = Decimal(avg_rating) * 20  # 5-star to 100%

    # Leave score: max penalty if leave_days > 5
    max_leave_penalty = Decimal(100)
    leave_penalty_score = max(Decimal(0), max_leave_penalty - (leave_days * 20))  # 5+ leaves = 0

    # Calculate final normalized score
    score = (
        (attendance_rate * attendance_rate_weight) +
        (punctuality_score * punctuality_score_weight) +
        (task_completion_rate * task_completion_rate_weight) +
        (leave_penalty_score * leave_penalty_weight) +
        (feedback_score * rating_weight)
    )

    grade = get_grade_for_score(score)

    performance, created = EmployeePerformance.objects.update_or_create(
        employee=employee,
        month=month.replace(day=1),
        defaults={
            'kpi': kpi,
            'hr_feedback': feedbacks.last(),
            'overall_score': score,
            'grade': grade
        }
    )
    assign_bonus_based_on_performance(employee, month)
    return performance
# --------------------------------------------------------------------------------------------------------------------------
from .models import EmployeePerformance, PerformanceBonusRule
from payroll.models import Payroll
from decimal import Decimal

def assign_bonus_based_on_performance(employee, month):
    try:
        perf = EmployeePerformance.objects.get(employee=employee, month=month)
        score = perf.overall_score

        # Get rule from DB (only one expected)
        rule = PerformanceBonusRule.objects.first()

        if rule and score >= rule.min_score_threshold:
            bonus = rule.bonus_amount
        else:
            bonus = Decimal('0')

        # Update payroll
        payroll, created = Payroll.objects.get_or_create(
            employee=employee,
            month=month.replace(day=1),
            defaults={'performance_bonus': bonus}
        )
        if not created:
            payroll.performance_bonus = bonus
            payroll.save()

        return bonus
    except EmployeePerformance.DoesNotExist:
        return None







# --------------------------------------------------------------------------------------------------------------------------
from .models import EmployeePerformance, TaskAssignment
from employees.models import Employee_data
from django.db.models import Avg
from datetime import date
from .forms import PerformanceBonusRuleForm
from .models import PerformanceBonusRule

def performance_dashboard(request):
    employees = Employee_data.objects.all()
    performance_data = []
    current_month = date.today().replace(day=1)
    for emp in employees:
        try:
            calculate_employee_performance(emp, current_month)
        except Exception as e:
            print(f"⚠️ Error calculating performance for {emp.employee_id}: {e}")

    total_attendance = 0
    total_task_completion = 0
    total_feedback = 0
    total_overall_score = 0
    total_tasks_count = 0
    employee_count = 0

    for emp in employees:
        try:
            performance = EmployeePerformance.objects.filter(employee=emp).latest('month')
            tasks = TaskAssignment.objects.filter(employee=emp)

            total_tasks = tasks.count()
            completed_tasks = tasks.filter(is_completed=True).count()
            task_completion = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            attendance = performance.kpi.attendance_rate
            
            feedback = performance.hr_feedback.rating if performance.hr_feedback else 0
            overall_score = performance.overall_score
            # print("KPI Raw Values:")
            # print(performance.kpi.__dict__)

            # Accumulate totals for average calculation
            total_attendance += attendance
            total_task_completion += task_completion
            total_feedback += feedback
            total_overall_score += overall_score
            total_tasks_count += total_tasks
            employee_count += 1

            performance_data.append({
                'employee': emp,
                'attendance_rate': round(attendance, 2),
                'task_completion': round(task_completion, 2),
                'avg_feedback': round(feedback, 2),
                'overall_score': round(overall_score, 2),
                'grade': performance.grade,
                'total_tasks': total_tasks,
            })
        except EmployeePerformance.DoesNotExist:
            continue

    # Calculate averages
    if employee_count > 0:
        avg_attendance = round(total_attendance / employee_count, 2)
        avg_task_completion = round(total_task_completion / employee_count, 2)
        avg_feedback = round(total_feedback / employee_count, 2)
        avg_score = round(total_overall_score / employee_count, 2)
    else:
        avg_attendance = avg_task_completion = avg_feedback = avg_score = 0

        # Get the existing rule instance or create a new one
    rule = PerformanceBonusRule.objects.first()
    form = PerformanceBonusRuleForm(instance=rule)

    monthly_scores = (
        EmployeePerformance.objects
        .values('month')
        .annotate(avg_score=Avg('overall_score'))
        .order_by('month')
    )

    kpi_months = [entry['month'].strftime('%b %Y') for entry in monthly_scores]
    kpi_scores = [round(entry['avg_score'], 2) for entry in monthly_scores]

    

    return render(request, 'performance.html', {
        'performance_data': performance_data,
        'avg_attendance': avg_attendance,
        'avg_task_completion': avg_task_completion,
        'avg_feedback': avg_feedback,
        'avg_score': avg_score,
        'employee_count': employee_count,
        'total_tasks_count': total_tasks_count,
        'form': form,
        'kpi_months': kpi_months,
        'kpi_scores': kpi_scores,
    })


# --------------------------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from .models import Task
from django.contrib import messages

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')

        if title:
            Task.objects.create(title=title, description=description)
            messages.success(request, "Task created successfully.")
            return redirect('create-task')

    # ✅ Always return a response, even for GET or failed POST
    return render(request, 'create_task.html')






def assign_task(request):
    tasks = Task.objects.all()
    employees = Employee_data.objects.all()

    if request.method == 'POST':
        task_id = request.POST.get('task')
        emp_id = request.POST.get('employee')
        due_date = request.POST.get('due_date')

        if task_id and emp_id and due_date:
            try:
                task = Task.objects.get(id=task_id)
                employee = Employee_data.objects.get(employee_id=emp_id)

                TaskAssignment.objects.create(task=task, employee=employee, due_date=due_date)
                return redirect('assign-task')
            except (Task.DoesNotExist, Employee_data.DoesNotExist):
                messages.error(request, "Invalid task or employee.")
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'assign_task.html', {
        'tasks': tasks,
        'employees': employees
    })

from django.shortcuts import get_object_or_404

def employee_task_view(request, employee_id):
    employee = get_object_or_404(Employee_data, employee_id=employee_id)
    tasks = TaskAssignment.objects.filter(employee=employee)

    return render(request, 'employee_task_detail.html', {
        'employee': employee,
        'tasks': tasks,
    })








from django.shortcuts import render, redirect
from django.utils import timezone
from .models import TaskAssignment

def mark_task_completed(request, task_assignment_id):
    # Fetch the task assignment using the given ID
    task_assignment = TaskAssignment.objects.get(id=task_assignment_id)

    # Update the completion status of the task
    task_assignment.is_completed = True
    task_assignment.completed_at = timezone.now()  # Set the completion date to current time
    task_assignment.save()

    return redirect('performance_dashboard')  # Redirect to the performance dashboard or the relevant page




# def submit_hr_feedback(request):
#     if request.method == 'POST':
#         employee_id = request.POST['employee']
#         rating = int(request.POST['rating'])
#         comments = request.POST.get('comments', '')

#         employee = Employee_data.objects.get(id=employee_id)
#         HRFeedback.objects.create(
#             employee=employee,
#             rating=rating,
#             comments=comments
#         )
#         return redirect('submit-feedback')

#     employees = Employee_data.objects.all()
#     return render(request, 'submit_feedback.html', {'employees': employees})



# from datetime import date

# def generate_monthly_performance(request):
#     current_month = date.today().replace(day=1)
#     employees = Employee_data.objects.all()
    
#     for employee in employees:
#         calculate_employee_performance(employee, current_month)

#     return render(request, 'performance_generated.html')



from .models import TeamPerformance

def generate_team_performance(request):
    from django.db.models import Avg

    current_month = date.today().replace(day=1)
    departments = Employee_data.objects.values_list('department', flat=True).distinct()

    for dept in departments:
        dept_emps = Employee_data.objects.filter(department=dept)
        avg_score = EmployeePerformance.objects.filter(
            employee__in=dept_emps,
            month=current_month
        ).aggregate(avg=Avg('overall_score'))['avg'] or 0

        TeamPerformance.objects.update_or_create(
            department=dept,
            month=current_month,
            defaults={
                'average_score': avg_score,
                'total_employees': dept_emps.count()
            }
        )

    team_data = TeamPerformance.objects.filter(month=current_month)

    return render(request, 'team_performance.html', {
        'team_data': team_data
    })





from django.shortcuts import render, redirect
from .models import PerformanceBonusRule
from .forms import PerformanceBonusRuleForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

def is_hr(user):
    # Replace this with your real HR check logic
    return user.is_authenticated and user.groups.filter(name='HR').exists()

@user_passes_test(is_hr)
def performance_bonus_settings(request):
    rule = PerformanceBonusRule.objects.first()

    if request.method == 'POST':
        form = PerformanceBonusRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return HttpResponse("Success")
            return redirect('performance_dashboard')  # Or wherever the modal is hosted
    else:
        form = PerformanceBonusRuleForm(instance=rule)

    return render(request, 'performance_dashboard.html', {'form': form})



from django.db.models import Avg
from django.http import JsonResponse

# def performance_chart_data(request):
    
#     return JsonResponse({
#         'months': kpi_months,
#         'scores': kpi_scores,
#     })


