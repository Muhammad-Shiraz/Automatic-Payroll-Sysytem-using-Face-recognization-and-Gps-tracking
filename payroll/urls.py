from django.urls import path
from . import views


urlpatterns = [
    path('', views.payroll_dashboard, name='payroll_dashboard'),
    path('employee/<str:employee_id>/', views.employee_payroll_detail, name='employee_payroll_detail'),
    path('api/refresh-payroll-dashboard/', views.api_refresh_payroll_dashboard, name='api_refresh_payroll_dashboard'),
    path('payroll_settings/', views.payroll_settings_view, name='payroll_settings'),
    path('api/payroll-chart/', views.payroll_chart_api, name='payroll_chart_api'),
    path('api/payroll-donut-chart/', views.payroll_chart_data, name='payroll_chart_data'),
    path('daily-salaries-api/', views.daily_salary_chart_api, name='daily_salaries_api'),

]
