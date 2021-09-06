from django import forms
from django.forms.widgets import HiddenInput
from .models import Lesson, Skill

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name','category']

class NewLessonForm(forms.ModelForm):

    day_choices = ( ("mon", "Monday"), 
                    ("tue", "Tuesday"), 
                    ("wed", "Wednesday"), 
                    ("thu", "Thursday"),
                    ("fri", "Friday"),
                    ("sat", "Saturday"),
                    ("sun", "Sunday")
                )
    day_selector = forms.MultipleChoiceField(
                                            choices=day_choices,
                                            widget=forms.CheckboxSelectMultiple,
                                            label="Available Teaching Days"
                                            )

    class Meta:
        model = Lesson
        fields = ['tutor','skill','skill_level','title','description','days','day_selector']
        widgets = { 
                    'tutor': forms.HiddenInput,
                    'days':forms.HiddenInput 
                }