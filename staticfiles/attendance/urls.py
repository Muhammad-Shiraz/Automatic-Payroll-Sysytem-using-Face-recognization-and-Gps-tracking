from django.urls import path
from . import views


urlpatterns = [
    path('real_time_attendance/', views.real_time_attendance, name='real_time_attendance'),
    path('all_attendance/',views.all_attendance,name='all_attendance'),
    path('profile_attendance/<int:employee_id>/',views.profile_attendance,name='profile_attendance'),
    path('delete_attendance/<int:record_id>/',views.delete_attendance,name='delete_attendance'),
    path("mark/", views.mark_attendance, name="mark_attendance"),
    path('present-chart-data/', views.present_employee_chart_data, name='present_employee_chart_data'),
    path('api/monthly-attendance-data/', views.monthly_attendance_chart_data, name='monthly_attendance_chart_data'),
    path('attendance-settings/', views.attendance_settings_view, name='attendance_settings'),
    path('manual-requests/', views.manage_manual_requests, name='manage_manual_requests'),
    path('manual-requests/approve/<int:request_id>/', views.approve_manual_attendance, name='approve_manual_attendance'),
    path('manual-requests/reject/<int:request_id>/', views.reject_manual_attendance, name='reject_manual_attendance'),
    path('manual-requests/all/', views.all_manual_requests, name='all_manual_requests'),
    
    
    
]
