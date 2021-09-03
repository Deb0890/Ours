from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'), 
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='log_out') 
]
