from django.urls import path
from django.contrib.auth import logout
from . import views

app_name = "feedback"

urlpatterns = [
    path("", views.redirect_after_login, name="redirect_after_login"),

    path("login/", views.StudentLoginView.as_view(), name="login"),
    path("logout/", views.StudentLogoutView.as_view(), name="logout"),
    path("register/", views.StudentRegisterView.as_view(), name="register"),

    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("new/", views.submit_feedback, name="submit_feedback"),
    path("history/", views.feedback_history, name="feedback_history"),
    path("detail/<int:pk>/", views.feedback_detail, name="feedback_detail"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("reports/", views.reports, name="reports"),

    path("faculty/", views.faculty_dashboard, name="faculty_dashboard"),
    path(
    "export/csv/",
    views.export_csv,
    name="export_csv",
),

path(
    "export/excel/",
    views.export_excel,
    name="export_excel",
),

path(
    "export/pdf/",
    views.export_pdf,
    name="export_pdf",
),
]