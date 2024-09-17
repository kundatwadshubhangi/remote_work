from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.Login_view, name='login'),
    path('user_logout', views.user_logout, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('index/', views.Index, name='index'),
    path('new_task/', views.create_task, name='new_task'),
    path('get_task_details/<int:task_id>/', views.get_task_details, name='get_task_details'),
    path('update_task_details/', views.update_task_details, name='update_task_details'),
]
