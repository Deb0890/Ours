from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/new', views.lesson_create, name="lesson-create"),
    path('lesson/<int:id>', views.lesson_detail_page, name="lesson-single"),
    path('lesson/find', views.find_a_lesson, name="find-a-lesson"),
    path('lesson/update/<int:id>', views.update_a_lesson, name="update-a-lesson"),
    path('lesson/delete/<int:id>',views.delete_a_lesson, name="delete-a-lesson")
]
