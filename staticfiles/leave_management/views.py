from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from datetime import date
from .models import LeaveRequest, OvertimeInvitation
from employees.models import Employee_data
from .forms import OvertimeAssignForm  # Yes, this is used!
from django.db.models import Count, Prefetch

# View to approve a leave or assign another employee to cover
@login_required
def approve_leave_view(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if request.method == 'POST':
        assigned_employee_id = request.POST.get('assigned_employee_id')
        if assigned_employee_id:
            assigned_emp = get_object_or_404(Employee_data, employee_id=assigned_employee_id)
            leave.assigned_employee = assigned_emp

        

        # Send approval email
        send_mail(
            'Your Leave Request was Approved',
            f'Dear {leave.employee.name}, your leave request from {leave.start_date} to {leave.end_date} has been approved.',
            'hr@yourcompany.com',
            [leave.employee.email],
            fail_silently=False,
        )
        messages.success(request, f"{leave.employee.name}Leave approve successfully!")
        # Approve the leave
        leave.emails_sent = True
        leave.status = 'Approved'
        leave.reviewed_on = timezone.now()
        leave.save()


    return redirect('leave-dashboard')

# View to assign overtime and send invitation emails
@login_required
def assign_overtime_view(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    department = leave.employee.department

    if request.method == 'POST':
        form = OvertimeAssignForm(department, request.POST)
        if form.is_valid():
            selected_employees = form.cleaned_data['employees']

            for emp in selected_employees:
                invitation = OvertimeInvitation.objects.create(leave=leave, employee=emp)
                confirm_url = request.build_absolute_uri(reverse('confirm_overtime', args=[invitation.id]))

                send_mail(
                    subject="Overtime Shift Assignment",
                    message=(
                        f"Dear {emp.name},\n\nYou're invited to cover for a colleague on leave.\n"
                        f"Please confirm your availability here: {confirm_url}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[emp.email],
                    fail_silently=False,
                )

            messages.success(request, "Overtime notifications sent successfully.")
            return redirect('leave-dashboard')
    else:
        form = OvertimeAssignForm(department)

    return render(request, 'assign_overtime.html', {'form': form, 'leave': leave})





@login_required
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    

    # Send email notification
    send_mail(
        'Your Leave Request was Rejected',
        f'Dear {leave.employee.name}, your leave request from {leave.start_date} to {leave.end_date} has been rejected.',
        'hr@yourcompany.com',  # Replace with your system email
        [leave.employee.email],
        fail_silently=False,
    )
    messages.success(request, "Leave Rejected!")
    leave.emails_sent = True
    leave.status = 'Rejected'
    leave.reviewed_on = timezone.now()
    leave.save()
    return redirect('leave-dashboard')  # Replace with your actual dashboard name


# Dashboard view showing leave status and today's approvals

from django.utils.timezone import now
@login_required
def leave_dashboard_view(request):
    # Prefetch invited employees per leave request
    invited_prefetch = Prefetch(
        'overtimeinvitation_set',
        queryset=OvertimeInvitation.objects.select_related('employee'),
        to_attr='invited_employees_list'
    )


    today = now().date()

    recent_leaves = LeaveRequest.objects.filter(
        applied_on__date=today  # ✅ This filters only today's leave applications
    ).select_related(
        'employee', 'leave_type', 'assigned_employee'
    ).prefetch_related(
        invited_prefetch
    ).order_by('-applied_on')[:10]


    leaverequest = LeaveRequest.objects.all()
    total_leaves = LeaveRequest.objects.count()
    total_approved = LeaveRequest.objects.filter(status='Approved').count()
    total_assigned = LeaveRequest.objects.filter(assigned_employee__isnull=False).count()

    leaves_by_status = LeaveRequest.objects.values('status').annotate(count=Count('id'))
    labels = [item['status'] for item in leaves_by_status]
    data = [item['count'] for item in leaves_by_status]


    context = {
        'leaverequest': leaverequest,
        'recent_leaves': recent_leaves,
        'total_leaves': total_leaves,
        'total_approved': total_approved,
        'total_assigned': total_assigned,
        'labels': labels,
        'data': data,
    }
    return render(request, 'leave_dashboard.html', context)


# View that handles employee confirming the overtime invitation
@login_required
def confirm_overtime_view(request, invitation_id):
    invitation = get_object_or_404(OvertimeInvitation, id=invitation_id)

    if not invitation.is_accepted:
        invitation.is_accepted = True
        invitation.responded_on = timezone.now()
        invitation.save()

        invitation.leave.assigned_employee = invitation.employee
        invitation.leave.save()

    return render(request, 'confirmation_success.html', {'employee': invitation.employee})

# Manual view to assign employee from dashboard radio buttons
@login_required
def assign_employee(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if request.method == 'POST':
        employee_id = request.POST.get('assigned_employee_id')
        if employee_id:
            assigned_emp = get_object_or_404(Employee_data, employee_id=employee_id)
            leave.assigned_employee = assigned_emp
            leave.save()
            messages.success(request, f"{assigned_emp.name} has been assigned to the leave.")
        else:
            messages.error(request, "No employee selected.")
        messages.success(request, "Employee added successfully!")
        return redirect('leave-dashboard')
