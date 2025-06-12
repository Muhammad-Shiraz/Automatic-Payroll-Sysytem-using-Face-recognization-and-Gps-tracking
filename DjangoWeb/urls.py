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

