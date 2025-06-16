# from employees.models import Employee_data  # adjust import if needed

def employee_context(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Employee").exists():
        try:
            employee = request.user.employee_data
            return {'employee': employee}
        except:
            return {}
    return {}
