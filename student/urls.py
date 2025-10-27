from django.urls import path
from . import views

urlpatterns = [
    path("exams/", views.ExamListView.as_view(), name="exam-list"),
    path("exams/<int:pk>/", views.ExamDetailView.as_view(), name="exam-detail"),
    path("exams/create/", views.ExamCreateView.as_view(), name="exam-create"),
    path("exams/<int:pk>/update/", views.ExamUpdateView.as_view(), name="exam-update"),
    path("exams/<int:pk>/delete/", views.ExamDeleteView.as_view(), name="exam-delete"),
]
