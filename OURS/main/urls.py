from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/new', views.lesson_create, name="lesson-create"),
    path('lesson/<int:id>', views.lesson_detail_page, name="lesson-single")
]
