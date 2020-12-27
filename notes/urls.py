from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
  path('profile/', views.get_user_profile, name='user_prof'),
  path('login/', views.AdminLogin.as_view(), name='login'),
  
  path('', views.home, name='home'),
]