# """
# URL configuration for DjangoWeb project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path , include
# from django.conf import settings
# from django.conf.urls.static import static
# from DjangoWeb import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.homePage, name='home'),
#     path('face/', views.live_camera_redirect, name='face'),
#     path('settings/', views.settings, name='settings'),
#     path('employee_dashboard/', include('employee_dashboard.urls')),
#     path('employees/', include('employees.urls')),
#     path('attendance/', include('attendance.urls')),
#     path("users/", include("users.urls")),
#     # path("dashboard/", views.dashboard_redirect, name="dashboard"),

# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from DjangoWeb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home Page - Redirects to the correct dashboard
    path('', views.home, name='home'),
    
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),

    # Face Recognition
    path('face/', views.live_camera_redirect, name='face'),

    # Settings Page
    path('settings/', views.settings, name='settings'),

    

    # Employee Management
    path('employees/', include('employees.urls')),

    # Attendance Management
    path('attendance/', include('attendance.urls')),

    # User Authentication
    path('users/', include('users.urls')),

    path('payroll/', include('payroll.urls')),

    path('performance/', include('performance.urls')),

    path('leave_management/', include('leave_management.urls')),

    path('complaints/', include('complaints.urls')),

    # Employee Dashboard URLs
    path('employee_dashboard/', include('employee_dashboard.urls')),
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

