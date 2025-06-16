from django.shortcuts import render, redirect, get_object_or_404
from datetime import date,datetime,timedelta
from django.utils import timezone
from django.contrib import messages
from .models import Employee_data, Attendance , Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import time
from django.contrib.auth.decorators import login_required

# --------------------- Daily Attendance ----------------------------------------------
@login_required
def real_time_attendance(request):
    selected_date = request.GET.get('date', date.today().isoformat())

    try:
        selected_date = date.fromisoformat(selected_date)
    except ValueError:
        selected_date = date.today()



    if request.method == "POST":
        attendance_id = request.POST.get("attendance_id")
        new_status = request.POST.get("status")
        new_time_in = request.POST.get("time_in")
        new_time_out = request.POST.get("time_out")

        if attendance_id and new_status:
            try:
                attendance = Attendance.objects.get(id=attendance_id)
                attendance.status = new_status

                # Update time_in and time_out only if provided
                if new_time_in:
                    attendance.time_in = new_time_in
                if new_time_out:
                    attendance.time_out = new_time_out
                # attendance.is_late = new_time_in > time(9, 0)

                attendance.save()
            except Attendance.DoesNotExist:
                print("Attendance record not found.")

        return redirect('real_time_attendance')

    employees = Employee_data.objects.all()
    attendance_queryset = Attendance.objects.filter(date=selected_date)
    total_employees = employees.count()  # Count employees
    attendance_records = {att.employee.employee_id: att for att in attendance_queryset}
    totalpresent = attendance_queryset.filter(status='Present').count()
    present_employee_ids = attendance_queryset.values_list('employee_id', flat=True)
    totalabsent = employees.exclude(employee_id__in=present_employee_ids).count()
    

    return render(request, 'real_time_attendance.html', {
        'employees': employees,
        'attendance_records': attendance_records,
        'selected_date': selected_date,
        'total_employees': total_employees,
        'totalpresent': totalpresent,
        'totalabsent': totalabsent
    })

# --------------------- All Profile Attendance ----------------------------------------------
@login_required
def all_attendance(request):
    employees = Employee_data.objects.all()
    attendance = Attendance.objects.all()
    return render(request, 'all_attendance.html', {
        'employees': employees, 
        'attendance': attendance,
        })


# --------------------- Profile wise Attendance ----------------------------------------------
@login_required
def profile_attendance(request,employee_id):
    employee = get_object_or_404(Employee_data, employee_id=employee_id)
    attendance = Attendance.objects.filter(employee=employee)

    return render(request, 'profile_attendance.html', {
        'employee': employee,
        'attendance': attendance,
    })

# --------------------- Delete Attendance ----------------------------------------------
@login_required
def delete_attendance(request, record_id):

    if request.method == 'POST':
        try:
            attendance_record = get_object_or_404(Attendance, id=record_id)  # Fetch attendance record
            attendance_record.delete()
            messages.success(request, "Attendance record deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting attendance record: {e}")  

    return redirect('all_attendance')  # Redirect to the attendance list page



# ----------------------------------------------------------------------------
@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        try:
            # ✅ Debug: Print raw request body
            raw_body = request.body.decode('utf-8')
            print(f"🔍 Raw Request Body: {raw_body}")

            data = json.loads(request.body)  # Parse JSON
            print("🔍 Parsed Data:", data)  # ✅ Debugging

            employee_id = data.get("employee_id")  # Ensure we use employee_id

            if not employee_id:
                print("❌ No employee ID provided!")
                return JsonResponse({"error": "No employee ID provided"}, status=400)

            # 🔹 Fix: Lookup employee using employee_id instead of name
            employee = Employee_data.objects.filter(employee_id=employee_id).first()

            if not employee:
                print(f"❌ Employee with ID '{employee_id}' not found!")
                return JsonResponse({"error": "Employee not found"}, status=404)

            if not employee.active_status:
                print(f"⛔ Employee '{employee_id}' is not active!")
                return JsonResponse({"error": "Employee is not active"}, status=403)

            today = date.today()
            now = datetime.now().time()

            location, _ = Location.objects.get_or_create(
                name="officeCam", defaults={"gps_coordinates": "31.5204,74.3587"}
            )

            attendance_entry = Attendance.objects.filter(employee=employee, date=today).first()

            if not attendance_entry:
                attendance_entry = Attendance.objects.create(
                    employee=employee,
                    time_in=now,
                    method='Auto',
                    location=location,
                    status='Present'
                )
                message = f"✅ Check-in marked for Employee ID {employee_id} at {now.strftime('%H:%M:%S')}"
            else:
                last_check_in_time = datetime.combine(today, attendance_entry.time_in)
                current_time = datetime.combine(today, now)

                if (current_time - last_check_in_time) >= timedelta(minutes=1):
                    attendance_entry.time_out = now
                    attendance_entry.save()
                    message = f"✅ Check-out updated for Employee ID {employee_id} at {now.strftime('%H:%M:%S')}"
                else:
                    message = f"⏳ Already checked in, no update needed."

            print("✅ Attendance Response:", message)
            return JsonResponse({"message": message}, status=200)

        except json.JSONDecodeError:
            print("❌ JSON Decode Error: Invalid JSON format")
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    print("❌ Invalid request method!")
    return JsonResponse({"error": "Invalid request method"}, status=405)




# -----------------------------------------------------------------------------------------------------------

@login_required
def present_employee_chart_data(request):
    today = timezone.now().date()
    data = []

    for i in range(6, -1, -1):  # Last 7 days
        day = today - timedelta(days=i)
        count = Attendance.objects.filter(date=day, status='Present').count()
        data.append({
            'date': day.strftime('%a'),  # Format like Mon, Tue...
            'present': count
        })

    return JsonResponse(data, safe=False)



from calendar import monthrange

from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Attendance

@login_required
def monthly_attendance_chart_data(request):
    data = (
        Attendance.objects
        .filter(status='Present')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(present_count=Count('id'))
        .order_by('month')
    )

    chart_data = {
        'labels': [entry['month'].strftime('%B %Y') for entry in data],
        'values': [entry['present_count'] for entry in data],
    }

    return JsonResponse(chart_data)



from django.shortcuts import render, get_object_or_404, redirect
from attendance.models import ManualAttendanceRequest, Attendance
from datetime import datetime
from django.contrib import messages

@login_required
def manage_manual_requests(request):
    requests = ManualAttendanceRequest.objects.filter(approved=False, rejected=False)
    return render(request, 'manage_manual_requests.html', {'requests': requests})



from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from attendance.models import Attendance, AttendanceSettings, ManualAttendanceRequest
from django.contrib.auth.decorators import login_required

@login_required
def approve_manual_attendance(request, request_id):
    req = get_object_or_404(ManualAttendanceRequest, id=request_id)

    # ⏰ Time now
    now = datetime.now()
    check_in = now.time()

    # ⏱ AttendanceSettings for shift duration
    settings = AttendanceSettings.objects.first()
    hours_per_day = float(settings.hours_per_day) if settings else 8.0

    # 🕘 Calculate check-out
    check_out_time = (now + timedelta(hours=hours_per_day)).time()

    print(f"🕓 Approved Check-in: {check_in}, Check-out: {check_out_time}")

    # 🧹 Remove old attendance (if any)
    Attendance.objects.filter(employee=req.employee, date=date.today()).delete()

    # ✅ Create fresh attendance record
    Attendance.objects.create(
        employee=req.employee,
        date=date.today(),
        time_in=check_in,
        time_out=check_out_time,
        method='Manual',
        status='Present',
        location=req.location
    )

    req.approved = True
    req.save()

    messages.success(request, f"Attendance approved. Check-in: {check_in}, Check-out: {check_out_time}")
    return redirect('manage_manual_requests')
@login_required
def reject_manual_attendance(request, request_id):
    req = get_object_or_404(ManualAttendanceRequest, id=request_id)
    req.rejected = True
    req.remarks = "Rejected by HR"
    req.save()
    messages.info(request, "Attendance rejected.")
    return redirect('manage_manual_requests')



@login_required
def all_manual_requests(request):
    all_requests = ManualAttendanceRequest.objects.select_related('employee').all().order_by('-submitted_at')
    return render(request, 'all_manual_requests.html', {'all_requests': all_requests})

from django.shortcuts import render, redirect
from .models import AttendanceSettings
from payroll.utils import get_daily_payroll_data 

def attendance_settings_view(request):
    # Always use the first or create the one and only settings record
    settings, _ = AttendanceSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        settings.shift_start = request.POST.get('shift_start')
        settings.shift_end = request.POST.get('shift_end')
        settings.working_days = request.POST.get('working_days')
        settings.hours_per_day = request.POST.get('hours_per_day')
        settings.overtime_rate = request.POST.get('overtime_rate')
        settings.save()
        get_daily_payroll_data()
        return redirect('attendance_settings')

    return render(request, 'attendance_settings.html', {'settings': settings})









