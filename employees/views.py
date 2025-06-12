from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee_data, Department, Designation
from .forms import DepartmentForm, DesignationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
import pickle
from django.conf import settings
import face_recognition
import os
import requests
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Employee_data
import calendar

@login_required
def employee_profile(request, employee_id):
    employee = get_object_or_404(Employee_data, employee_id=employee_id)
    return render(request, 'employee_profile.html', {'employee': employee})



@login_required
def create_employee(request):
    # Fetch departments and designations
    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == 'POST':
        # Retrieve the data from the form
        # employee_id = request.POST.get('employeeID')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postalCode')
        country = request.POST.get('country')
        department_id = request.POST.get('department')  
        shift = request.POST.get('shift')
        employment_type = request.POST.get('employmentType')
        active_status = request.POST.get("active_status", "False") == "True"
        

        salary = request.POST.get('salary', '0')  # Default salary to '0' if empty
        designation_id = request.POST.get('designation')  
        joining_date = request.POST.get('joining_date')
        bank_account_number = request.POST.get('bankAccount')
        bank_name = request.POST.get('bankName')
        emergency_contact_name = request.POST.get('emergencyContactName')
        emergency_contact_relationship = request.POST.get('emergencyContactrelationship')
        emergency_contact_phone = request.POST.get('emergencyContactPhone')
        employee_images = request.FILES.get('employee_images')

        # Fetch related department and designation
        try:
            department = Department.objects.get(id=department_id)
        except ObjectDoesNotExist:
            return render(request, 'create_employee.html', {
                'departments': departments,
                'designations': designations,
                'error_message': 'Selected department does not exist.'
            })

        try:
            designation = Designation.objects.get(id=designation_id)
        except ObjectDoesNotExist:
            return render(request, 'create_employee.html', {
                'departments': departments,
                'designations': designations,
                'error_message': 'Selected designation does not exist.'
            })

        # Check if the user already exists
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': name}
        )

        if created:
            user.set_password(password)  
            user.save()

            # Assign Employee role
            employee_group, _ = Group.objects.get_or_create(name='Employee')
            user.groups.add(employee_group)

        # Create and save the Employee data
        employee = Employee_data(
            # employee_id=employee_id,
            user=user,
            name=name,
            email=email,
            password=password,  
            dob=dob,
            phone_number=phone_number,
            gender=gender,
            marital_status=marital_status,
            street=street,
            city=city,
            state=state,
            postalCode=postal_code,
            country=country,
            department=department,
            shift=shift,
            employmentType=employment_type,
            active_status=active_status,
            salary=salary,  # Fixed salary issue
            designation=designation,
            joining_date=joining_date,
            bankAccount=bank_account_number,
            bankName=bank_name,
            emergencyContactName=emergency_contact_name,
            emergencyContactrelationship=emergency_contact_relationship,
            emergencyContactPhone=emergency_contact_phone,
            employee_images=employee_images
        )

        # Save the employee to the database
    
        employee.save()

        # Update the face encodings pickle file
        if employee_images:
        # Path to the pickle file (store at BASE_DIR)
            flask_app_path = os.path.join(settings.BASE_DIR, 'flask_camera_service')  
            pickle_file_path = os.path.join(flask_app_path, 'employee_faces.pkl')
            os.makedirs(flask_app_path, exist_ok=True)
            # Ensure the file exists before reading
            if not os.path.exists(pickle_file_path):
                with open(pickle_file_path, 'wb') as file:
                    pickle.dump({}, file)  # Create an empty dictionary

            # Load existing encodings
            with open(pickle_file_path, 'rb') as file:
                face_data = pickle.load(file)

            # Build the full path to the new employee image
            image_path = os.path.join(settings.MEDIA_ROOT, str(employee.employee_images))
            if os.path.exists(image_path):
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    # Store encoding using Employee ID as the key
                    face_data[str(employee.employee_id)] = encodings[0]
                    print(f"✅ Updated encoding for Employee ID {employee.employee_id}")
                else:
                    print(f"⚠️ No face encoding found for Employee ID {employee.employee_id}")
            else:
                print(f"⚠️ Image file not found: {image_path}")

            # Save the updated face_data back to the pickle file
            with open(pickle_file_path, 'wb') as file:
                pickle.dump(face_data, file)
                # Redirect to the employee creation page after success
                return redirect('create_employee')
        

    return render(request, 'create_employee.html', {
        'departments': departments,
        'designations': designations
    })


@login_required
def employee_list(request):
    employees = Employee_data.objects.all()
    total_employees = employees.count()  # Count employees
    active_employees = employees.filter(active_status=True).count()  
    departmant = Department.objects.all()
    total_departmant = departmant.count()
    return render(request, 'employee_list.html', {'employees': employees, 'total_employees': total_employees, 'active_employees': active_employees,'total_departmant':total_departmant})


def notify_flask_to_reload():
    """Notify the Flask app to reload encodings after an update."""
    FLASK_RELOAD_URL = "http://127.0.0.1:5001/reload_encodings"
    try:
        response = requests.post(FLASK_RELOAD_URL)
        if response.status_code == 200:
            print("✅ Flask successfully reloaded encodings.")
        else:
            print(f"⚠️ Flask reload error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not contact Flask: {e}")     
            
def update_employee_encodings(employee):
    """Update the face encoding when an employee's image is changed."""
    flask_app_path = os.path.join(settings.BASE_DIR, 'flask_camera_service')
    pickle_file_path = os.path.join(flask_app_path, 'employee_faces.pkl')

    # Load existing encodings
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, 'rb') as file:
            face_data = pickle.load(file)
    else:
        face_data = {}

    # ✅ Remove old encoding if it exists
    if str(employee.employee_id) in face_data:
        del face_data[str(employee.employee_id)]  # Remove old face data
        print(f"🗑 Removed old encoding for Employee ID {employee.employee_id}")

    # ✅ Get new image path
    image_path = os.path.join(settings.MEDIA_ROOT, str(employee.employee_images))
    if os.path.exists(image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            face_data[str(employee.employee_id)] = encodings[0]  # Save new encoding
            print(f"✅ Updated encoding for Employee ID {employee.employee_id}")
        else:
            print(f"⚠️ No face encoding found for Employee ID {employee.employee_id}")

    # ✅ Save updated face encodings
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(face_data, file)

    # ✅ Notify Flask to reload new encodings
    notify_flask_to_reload()
@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee_data, employee_id=employee_id)
    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == 'POST':
        try:
            print("Received POST Data:", request.POST)  # Debugging
            employee.name = request.POST.get('name', employee.name)
            employee.email = request.POST.get('email', employee.email)
            employee.phone_number = request.POST.get('phone', employee.phone_number)
            employee.dob = request.POST.get('dob', employee.dob)

            # Address Details
            employee.street = request.POST.get('street', employee.street)
            employee.city = request.POST.get('city', employee.city)
            employee.state = request.POST.get('state', employee.state)
            employee.postal_code = request.POST.get('postal_code', employee.postalCode)
            employee.country = request.POST.get('country', employee.country)

            # Job Details
            employee.salary = float(request.POST.get('salary', employee.salary)) if request.POST.get('salary') else employee.salary
            employee.shift = request.POST.get('shift', employee.shift)
            employee.employmentType = request.POST.get('employmentType', employee.employmentType)
            employee.active_status = request.POST.get('active_status') == 'True'

            department_id = request.POST.get('department')
            designation_id = request.POST.get('designation')

            if department_id:
                employee.department = Department.objects.get(id=department_id)
            if designation_id:
                employee.designation = Designation.objects.get(id=designation_id)

            employee.bankAccount = request.POST.get('bankAccount', employee.bankAccount)
            employee.bankName = request.POST.get('bankName', employee.bankName)

            employee.emergencyContactName = request.POST.get('emergencyContactName', employee.emergencyContactName)
            employee.emergencyContactrelationship = request.POST.get('emergencyContactrelationship', employee.emergencyContactrelationship)
            employee.emergencyContactPhone = request.POST.get('emergencyContactPhone', employee.emergencyContactPhone)
            
            new_image = request.FILES.get('employee_images')

            if new_image:
                # ✅ Delete the old image file if it exists
                if employee.employee_images:
                    old_image_path = os.path.join(settings.MEDIA_ROOT, str(employee.employee_images))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)  # Delete the old image file
                        print(f"🗑 Deleted old image: {old_image_path}")

                # ✅ Rename new image to employee ID (e.g., `E123.jpg`)
                extension = new_image.name.split('.')[-1]
                new_image.name = f"{employee.employee_id}.{extension}"
                employee.employee_images = new_image

            employee.save()

            # ✅ Update face encodings properly
            if new_image:
                update_employee_encodings(employee)

            messages.success(request, "Employee updated successfully!")
            return redirect('employee_list')

        except Exception as e:
            messages.error(request, f"Error updating employee: {e}")
            print("Update Employee Error:", e)

    return render(request, 'edit_employee.html', {
        'employee': employee,
        'departments': departments, 
        'designations': designations
    })


@login_required
def delete_employee(request, employee_id):

    """Delete an employee from the database"""
    if request.method == 'POST':
        try:
            employee = get_object_or_404(Employee_data, employee_id=employee_id)
            employee.delete()
            messages.success(request, "Employee deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting employee: {e}")  


    return redirect('employee_list')




# ================================ Active status ======================================
def update_employee_status(request, emp_id):
    # Use `employee_id` instead of `id`
    employee = get_object_or_404(Employee_data, employee_id=emp_id)

    if request.method == "POST":
        employee.active_status = not employee.active_status
        employee.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))



def employee_monthly_joining(request):
    data = (
        Employee_data.objects
        .filter(joining_date__isnull=False)
        .annotate(month=TruncMonth('joining_date'))
        .values('month')
        .annotate(count=Count('employee_id'))
        .order_by('month')
    )

    labels = []
    counts = []
    for entry in data:
        month_name = calendar.month_abbr[entry['month'].month]
        labels.append(month_name)
        counts.append(entry['count'])

    return JsonResponse({'labels': labels, 'data': counts})






# views.py
from django.shortcuts import render, redirect
from .models import Department, Designation,Employee_data
from .forms import DepartmentForm, DesignationForm

def manage_dept_designation(request):
    departments = Department.objects.all()
    designations = Designation.objects.all()

    dept_form = DepartmentForm()
    desig_form = DesignationForm()

    if request.method == 'POST':
        if 'dept-submit' in request.POST:
            dept_form = DepartmentForm(request.POST)
            if dept_form.is_valid():
                dept_form.save()
                return redirect('manage_dept_desig')
        elif 'desig-submit' in request.POST:
            desig_form = DesignationForm(request.POST)
            if desig_form.is_valid():
                desig_form.save()
                return redirect('manage_dept_desig')
        elif 'delete-dept-id' in request.POST:
            dept_id = request.POST.get('delete-dept-id')
            Department.objects.filter(id=dept_id).delete()
            return redirect('manage_dept_desig')
        elif 'delete-desig-id' in request.POST:
            desig_id = request.POST.get('delete-desig-id')
            Designation.objects.filter(id=desig_id).delete()
            return redirect('manage_dept_desig')

    # Annotate with employee counts
    department_data = [
        {
            'obj': dept,
            'employee_count': Employee_data.objects.filter(department=dept).count()
        }
        for dept in departments
    ]

    designation_data = [
        {
            'obj': desig,
            'employee_count': Employee_data.objects.filter(designation=desig).count()
        }
        for desig in designations
    ]

    return render(request, 'manage_dept_desig.html', {
        'dept_form': dept_form,
        'desig_form': desig_form,
        'departments': department_data,
        'designations': designation_data,
    })


