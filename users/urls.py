from django.urls import path
from .views import register, admin_dashboard, user_tasks, user_dashboard

urlpatterns = [
    path('', register, name='register'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/<int:user_id>/tasks/', user_tasks, name='user_tasks'),
]