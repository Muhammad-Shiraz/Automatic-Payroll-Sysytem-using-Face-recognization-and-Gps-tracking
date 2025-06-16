from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Automatically detect group
            if user.groups.filter(name="HR").exists():
                return redirect('hr_dashboard')  # Change to your actual HR dashboard URL name
            elif user.groups.filter(name="Employee").exists():
                return redirect('emp_dashboard')  # Change to your employee dashboard URL name
            else:
                # If user doesn't belong to any group
                return render(request, 'login.html', {'error': 'User has no assigned role.'})
        
        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')
