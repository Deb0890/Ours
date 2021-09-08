from .models import Classroom, Review, User
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
        review = Review.objects.filter(id=classroom.id)
        if review.tutor_void and review.student_void:
            return
        else:
            student = User.objects.filter(id=classroom.student.id)    
            tutor = User.objects.filter(id=classroom.skill.tutor.id)
            student.profile.classroom_complete += 1
            student.profile.rating += review.tutor_review_score
            student.profile.dollours -= 1
            tutor.profile.classroom_complete += 1
            tutor.profile.rating += review.student_review_score
            tutor.profile.dollours += 1
            classroom.state = "CL"
            student.save()
            tutor.save()
            classroom.save()    
