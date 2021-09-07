from django import forms
from django.forms import fields, widgets
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError
from .models import Classroom, Lesson, Skill
import calendar
from django.utils import timezone

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

class DateInput(forms.DateInput):
    input_type = 'date'

class NewClassroomForm(forms.ModelForm):

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
                                            label="Available Teaching Days",
                                            required=False
                                            )

    day_selector.widget.attrs['disabled'] = True

    class Meta:
        model = Classroom
        fields = ['lesson','day_selector','time','student']
        labels = {
            'time': 'Date',
        }
        widgets = {
            'student': forms.HiddenInput,
            'time': DateInput()
        }

    def clean_time(self):
        data = self.cleaned_data['time']
        available_days = self.cleaned_data['lesson'].days
        day = calendar.day_abbr[data.weekday()]
        if day.lower() not in available_days:
            raise ValidationError("You have chosen a day where the Tutor is unavailable")
        if data < timezone.now():
            raise ValidationError("Cannot book classrooms in the past")
        return data

class UpdateClassroomForm(forms.ModelForm):

    date = forms.Field(
        widget=forms.widgets.DateInput(attrs={'type':'date'}),
        label='Date'
    )
    date.widget.attrs['readonly'] = True

    time = forms.Field(
        widget=forms.widgets.TimeInput(attrs={'type':'time'}),
        label='Time'
    )

    notes = forms.Field(
        widget=forms.widgets.Textarea(),
        required=False
    )

    class Meta:
        model = Classroom
        fields = ['date','time','notes']

class FinaliseClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_details']