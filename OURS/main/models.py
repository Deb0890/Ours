from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Categories"

class Skill(models.Model):
    name = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

class SkillLevels(models.TextChoices):
    BEGINNER = 'B', 'Beginner'
    INTERMEDIATE = 'I', 'Intermediate'
    ADVANCED = 'A', 'Advanced'

class Lesson(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)
    skill_level = models.CharField(
        max_length=1,
        choices=SkillLevels.choices,
        default=SkillLevels.BEGINNER,
    )
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(max_length=1024,blank=True,null=True)
    banner_img = models.ImageField(upload_to='lessons',blank=True,null=True)
    days = models.CharField(max_length=100,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.skill.name} ({self.get_skill_level_display()})'

class ClassroomState(models.TextChoices):
    CREATED = 'CR', 'Created'
    AWAITING = 'AC', 'Awaiting Confirmation'
    CONFIRMED = 'CF', 'Confirmed'
    UPCOMING = 'UP', 'Upcoming'
    COMPLETE = 'CP', 'Complete'
    PARTREVIEW = 'PR', 'Part Reviewed'
    FULLREVIEW = 'FR', 'Fully Reviewed'
    CLOSED = 'CL', 'Closed'

class Classroom(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.CharField(
        max_length=2,
        choices=ClassroomState.choices,
        default=ClassroomState.CREATED,
    )
    time = models.DateTimeField(blank=True, null=True)
    room_details = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.lesson.skill} -> Tutor: {self.lesson.tutor}, Student: {self.student}, State: {self.get_state_display()}'

class ClassroomNote(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    classroom = models.OneToOneField(Classroom, on_delete=models.CASCADE)
    tutor_review_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True, null=True)
    tutor_review_time = models.DateTimeField(blank=True, null=True)
    student_review_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True, null=True)
    student_review_time = models.DateTimeField(blank=True, null=True)
    tutor_void = models.BooleanField(default=False)
    student_void = models.BooleanField(default=False)

@receiver(post_save, sender=Classroom)
def create_classroom_review(sender, instance, created, **kwargs):
    if created:
        Review.objects.create(classroom=instance)

@receiver(post_save, sender=Classroom)
def save_classroom_review(sender, instance, **kwargs):
    instance.review.save()