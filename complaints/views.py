from django.shortcuts import render, redirect
from performance.models import HRFeedback
from employees.models import Employee_data
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from performance.models import HRFeedback
from employees.models import Employee_data
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from employees.models import Employee_data  # your Employee model

def hr_feedback_view(request):
    employees = Employee_data.objects.all()  # fetch all employees

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")

        # Validate employee exists
        try:
            employee = Employee_data.objects.get(employee_id=employee_id)
        except Employee_data.DoesNotExist:
            employee = None

        if employee:
            # Create HRFeedback object (example model)
            HRFeedback.objects.create(
                employee=employee,
                rating=rating,
                comments=comments,
            )
            return redirect('feedback_thank_you')  # redirect after POST

    context = {
        "employees": employees,
    }
    return render(request, "submit_feedback.html", context)




@login_required
def feedback_thank_you(request):
    return render(request, 'thank_you.html')



from django.shortcuts import render
from .models import Complaint, EmployeeFeedback
from django.contrib.auth.decorators import login_required

@login_required
def view_complaints_hr(request):
    complaints = Complaint.objects.select_related('employee').order_by('-date_submitted')
    feedbacks = EmployeeFeedback.objects.select_related('employee').order_by('-submitted_at')
    return render(request, 'view_complaints.html', {
        'complaints': complaints,
        'feedbacks': feedbacks
    })

