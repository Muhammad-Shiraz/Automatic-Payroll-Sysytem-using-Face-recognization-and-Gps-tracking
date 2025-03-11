from django.urls import path
from . import views


urlpatterns = [
    path('real_time_attendance/', views.real_time_attendance, name='real_time_attendance'),
    path('all_attendance/',views.all_attendance,name='all_attendance'),
    path('profile_attendance/<int:employee_id>/',views.profile_attendance,name='profile_attendance'),
    path('delete_attendance/<int:record_id>/',views.delete_attendance,name='delete_attendance'),
    path("mark/", views.mark_attendance, name="mark_attendance"),
    
]
