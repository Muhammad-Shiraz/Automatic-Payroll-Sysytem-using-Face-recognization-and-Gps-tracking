from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required
def employee_dashboard(request):
    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_dashboard.html')
    else:
        return redirect('unauthorized_page')


