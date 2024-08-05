from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.Login_view, name='login'),
    path('user_logout', views.user_logout, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('index', views.Index, name='index'),
]
