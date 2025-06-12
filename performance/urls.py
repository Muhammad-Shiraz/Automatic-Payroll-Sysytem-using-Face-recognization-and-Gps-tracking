from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.performance_dashboard, name='performance_dashboard'),
    path('create-task/', views.create_task, name='create-task'),
    path('assign-task/', views.assign_task, name='assign-task'),
    path('employee/<int:employee_id>/tasks/', views.employee_task_view, name='employee-task-view'),
    path('mark-task-completed/<int:task_assignment_id>/', views.mark_task_completed, name='mark-task-completed'),
    path('generate-team-performance/', views.generate_team_performance, name='generate-team-performance'),
    path('bonus-settings/', views.performance_bonus_settings, name='performance_bonus_settings'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)