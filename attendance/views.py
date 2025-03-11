from django.shortcuts import render, redirect, get_object_or_404
from datetime import date,datetime,timedelta
from django.contrib import messages
from .models import Employee_data, Attendance , Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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


# ------------------ Attendance marked using face recognization ....Django Api --------------

# @csrf_exempt
# def mark_attendance(request):
#     if request.method == "POST":
#         try:
#             # ✅ Debug: Print raw request body
#             raw_body = request.body.decode('utf-8')
#             print(f"🔍 Raw Request Body: {raw_body}")

#             data = json.loads(request.body)  # Parse JSON
#             print("🔍 Parsed Data:", data)  # ✅ Debugging

#             employee_id = data.get("name") or data.get("employee_id")

#             if not employee_id:
#                 print("❌ No employee name provided!")
#                 return JsonResponse({"error": "No employee name provided"}, status=400)

#             employee = Employee_data.objects.filter(name=employee_id).first()

#             if not employee:
#                 print(f"❌ Employee '{employee_id}' not found!")
#                 return JsonResponse({"error": "Employee not found"}, status=404)

#             if not employee.active_status:
#                 print(f"⛔ Employee '{employee_id}' is not active!")
#                 return JsonResponse({"error": "Employee is not active"}, status=403)

#             today = date.today()
#             now = datetime.now().time()

#             location, _ = Location.objects.get_or_create(name="officeCam", defaults={"gps_coordinates": "31.5204,74.3587"})

#             attendance_entry = Attendance.objects.filter(employee_id=employee, date=today).first()

#             if not attendance_entry:
#                 attendance_entry = Attendance.objects.create(
#                     employee_id=employee,
#                     time_in=now,
#                     method='Auto',
#                     location=location,
#                     status='Present'
#                 )
#                 message = f"✅ Check-in marked for {employee_id} at {now.strftime('%H:%M:%S')}"
#             else:
#                 last_check_in_time = datetime.combine(today, attendance_entry.time_in)
#                 current_time = datetime.combine(today, now)

#                 if (current_time - last_check_in_time) >= timedelta(minutes=1):
#                     attendance_entry.time_out = now
#                     attendance_entry.save()
#                     message = f"✅ Check-out updated for {employee_id} at {now.strftime('%H:%M:%S')}"
#                 else:
#                     message = f"⏳ Already checked in, no update needed."

#             print("✅ Attendance Response:", message)
#             return JsonResponse({"message": message}, status=200)

#         except json.JSONDecodeError:
#             print("❌ JSON Decode Error: Invalid JSON format")
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     print("❌ Invalid request method!")
#     return JsonResponse({"error": "Invalid request method"}, status=405)

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
