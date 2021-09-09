from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'), 
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,template_name='auth/login.html'), name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html',next_page='homepage'), name='log_out'), 
    path('profile/',views.update_profile, name='update_profile'),
    path('profile/<int:id>',views.get_profile, name='single_profile'),
    path('profile-delete/',views.delete_profile, name='delete_profile'),
]
