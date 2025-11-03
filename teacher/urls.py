from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.TeacherLoginView.as_view(), name='teacher-login'),
    path('api/login/', views.teacher_login_api, name='teacher-login-api'),
    path('dashboard/', views.TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('create-exam/', views.CreateExamView.as_view(), name='teacher-create-exam'),
    path('api/create-exam/', views.create_exam_api, name='teacher-create-exam-api'),
    path('upload-paper/', views.UploadPaperView.as_view(), name='teacher-upload-paper'),
    path('api/upload-paper/', views.upload_paper_api, name='teacher-upload-paper-api'),
    path('manage-exams/', views.ManageExamsView.as_view(), name='teacher-manage-exams'),
]

