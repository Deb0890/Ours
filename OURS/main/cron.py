from .models import Classroom, Review
from django.contrib.auth.models import User
from django.utils import timezone

def my_cron_job():
    # your functionality goes here
    classrooms = Classroom.objects.filter(state="UP",time__lte=timezone.now())
    for classroom in classrooms:
        classroom.state = "CP"
        classroom.save()

def close_rooms_cron_job():
    classrooms = Classroom.objects.filter(state="FR")
    for classroom in classrooms:
        review = Review.objects.get(id=classroom.id)
        student = User.objects.get(id=classroom.student.id)    
        tutor = User.objects.get(id=classroom.lesson.tutor.id)
        student.profile.classroom_complete += 1
        student.profile.score += review.tutor_review_score
        student.profile.dollours -= 1
        tutor.profile.classroom_complete += 1
        tutor.profile.score += review.student_review_score
        tutor.profile.dollours += 1
        classroom.state = "CL"
        student.save()
        tutor.save()
        classroom.save()    
