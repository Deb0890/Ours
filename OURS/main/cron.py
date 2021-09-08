from .models import Classroom
from datetime import datetime

def my_cron_job():
    # your functionality goes here
    classrooms = Classroom.objects.filter(state="UP",time__lte=datetime.now())
    for classroom in classrooms:
        classroom.state = "CP"
        classroom.save()