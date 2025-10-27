from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.ExamListView.as_view(), name='exam-list'),
    path('exams/<int:id>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('test-papers/<int:id>/', views.TestPaperDetailView.as_view(), name='test-paper-detail'),
    path('questions/mcq/<int:id>/', views.QuestionTypeMCQDetailView.as_view(), name='question-mcq-detail'),
    path('questions/numerical/<int:id>/', views.QuestionTypeNumericalDetailView.as_view(), name='question-numerical-detail'),
    path('questions/msq/<int:id>/', views.QuestionTypeMSQDetailView.as_view(), name='question-msq-detail'),
    path('add-exam/', views.add_exam, name='add-exam'),
    path('add-test-paper/', views.add_test_paper, name='add-test-paper'),
    path('view-exams/', views.view_exams, name='view-exams'),
    path('view-test-papers/', views.view_test_papers, name='view-test-papers'),
]