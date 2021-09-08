from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/new', views.lesson_create, name="lesson-create"),
    path('lesson/<int:id>', views.lesson_detail_page, name="lesson-single"),
    path('lesson/find', views.find_a_lesson, name="find-a-lesson"),
    path('lesson/update/<int:id>', views.update_a_lesson, name="update-a-lesson"),
    path('lesson/delete/<int:id>',views.delete_a_lesson, name="delete-a-lesson"),
    path('classroom/new/<int:id>',views.classroom_create, name="classroom-create"),
    path('classroom/update/<int:id>',views.classroom_update, name="classroom-update"),
    path('classroom/finalise/<int:id>',views.classroom_finalise, name="classroom-finalise"),
    path('classroom/confirm/<int:id>',views.classroom_confirm, name="classroom-confirm"),
    path('classroom/<int:id>',views.classroom_detail, name="classroom-single")
]
