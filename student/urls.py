from django.urls import path
from . import views

urlpatterns = [
    path("my-exams/", views.MyExamsView.as_view(), name="my-exams"),
    path("results/", views.ResultsView.as_view(), name="results"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("update-profile/", views.update_profile, name="update-profile"),
    path("api/dashboard-data/", views.dashboard_data, name="dashboard-data"),
]
