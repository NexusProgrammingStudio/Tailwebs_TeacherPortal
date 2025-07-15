from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_login, name='login'),
    path('logout/', views.teacher_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-or-update-student/', views.add_or_update_student, name='add_student'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
]
