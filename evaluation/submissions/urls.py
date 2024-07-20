from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.submissions_dashboard, name="dashboard"),
    path('submission/student/<int:pk>', views.submission_student_detail, name="submission_student_detail"),
    path('submission/student/review/<int:course_id>', views.submission_student_create, name="submission_student_create"),
    #path('submission/supervisor/<int:pk>', views.submission_supervisor_detail, name="submission_supervisor_detail"),
    #path('submission/supervisor/review/<int:course_id>', views.submission_supervisor_create, name="submission_supervisor_create"),
    path('', views.submissions_landing, name="landing"),
]
