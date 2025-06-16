from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.hr_feedback_view, name='hr_feedback_view'),
    path('thank-you/', views.feedback_thank_you, name='feedback_thank_you'),
    path('view-complaints/', views.view_complaints_hr, name='view_complaints_hr'),
]
