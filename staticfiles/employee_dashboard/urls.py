from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='emp_dashboard'),
    path('submit-manual/', views.submit_manual_attendance, name='submit_manual_attendance'),
    path('emp_performance/', views.employee_performance_dashboard, name='emp_performance'),
    path('tasks/', views.employee_task, name='employee_tasks'),
    path('emp_attendance/', views.emp_attendance, name='emp_attendance'),
    path('analytics/', views.attendance_analytics, name='attendance_analytics'),
    path('payroll/', views.employee_payroll_view, name='employee_payroll'),
    path('payroll/daily/<str:month>/', views.daily_payroll_view, name='daily_payroll_view'),
    path("generate-slip/", views.generate_payroll_slip, name="generate_payroll_slip"),
    path('payroll/slip/', views.payroll_slip, name='payroll_slip'),
    path('request-leave/', views.emp_leave_request, name='emp_leave_request'),
    path('my-leaves/', views.my_leave_requests, name='my_leave_requests'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('feedback/', views.employee_feedback_view, name='employee_feedback'),
    path('update-profile/', views.update_employee_profile, name='update_employee_profile'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)