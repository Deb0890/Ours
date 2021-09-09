from django.contrib import admin
from .models import Category, Lesson, Skill, Classroom, ClassroomNote, Review

# Register your models here.
admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Lesson)
admin.site.register(Classroom)
admin.site.register(ClassroomNote)
admin.site.register(Review)