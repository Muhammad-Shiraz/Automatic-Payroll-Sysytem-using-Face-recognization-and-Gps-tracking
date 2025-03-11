from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group  # Import Django Groups

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # Get selected role (HR or Employee)

        user = authenticate(request, username=username, password=password)
        
        if user:
            if (role == "HR" and user.groups.filter(name="HR").exists()) or \
               (role == "Employee" and user.groups.filter(name="Employee").exists()):
                
                login(request, user)
                return redirect('/')  # Redirect to home (it will auto-load the correct dashboard)
            
            else:
                return render(request, 'login.html', {'error': 'Invalid role selected'})
        
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')
