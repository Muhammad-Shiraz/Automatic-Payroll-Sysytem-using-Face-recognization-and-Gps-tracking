from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('create_employee/',views.create_employee, name='create_employee'),
    path('employee_list/',views.employee_list, name='employee_list'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employee_profile/<int:employee_id>/', views.employee_profile, name='employee_profile'),
    path('add-department/', views.add_department, name='add_department'),
    path('add-designation/', views.add_designation, name='add_designation'),
    path('update-employee-status/<int:emp_id>/', views.update_employee_status, name='update_employee_status'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
