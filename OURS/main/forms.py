from django import forms
from django.forms.widgets import HiddenInput 
from .models import Lesson, Skill

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name','category']

class NewLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['tutor','skill','skill_level','title','description','banner_img']
        widgets = { 'tutor': forms.HiddenInput }