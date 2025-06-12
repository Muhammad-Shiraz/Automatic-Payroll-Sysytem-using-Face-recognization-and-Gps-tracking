from django.urls import path
from . import views


urlpatterns = [
    path('leave-dashboard/', views.leave_dashboard_view, name='leave-dashboard'),
    path('approve/<int:leave_id>/', views.approve_leave_view, name='approve_leave'),
    path('confirm-overtime/<int:invitation_id>/', views.confirm_overtime_view, name='confirm_overtime'),
    path('assign-overtime/<int:leave_id>/', views.assign_overtime_view, name='assign_overtime'),
    path('assign/<int:leave_id>/', views.assign_employee, name='assign_employee'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),

]