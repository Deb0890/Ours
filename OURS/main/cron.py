from .models import Classroom
from django.utils import timezone

def my_cron_job():
    # your functionality goes here
    classrooms = Classroom.objects.filter(state="UP",time__lte=timezone.now())
    for classroom in classrooms:
        classroom.state = "CP"
        classroom.save()