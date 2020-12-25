from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("user", views.user_view, name="user"),
    path("addPage", views.add_page, name="addPage"),
    path("removePage", views.remove_page, name="remove_page"),
    path("report", views.report_view, name="report"),
    path("settings", views.settings_view, name="settings"),
    path("processReport", views.process_report, name="processReport"),
    path("pageData/<int:page_id>", views.page_data, name="pageData")
]