from django import forms
from django.forms import fields, widgets
from django.forms.widgets import HiddenInput, Widget
from django.core.exceptions import ValidationError
from .models import Classroom, Lesson, Skill, Review
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


    def __init__(self, *args, **kwargs):
        super(NewClassroomForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # self.fields['lesson'].disabled = True


    day_choices = ( ("mon", "Monday"), 
                    ("tue", "Tuesday"), 
                    ("wed", "Wednesday"), 
                    ("thu", "Thursday"),
                    ("fri", "Friday"),
                    ("sat", "Saturday"),
                    ("sun", "Sunday")
                )
    day_selector = forms.MultipleChoiceField (
                                        choices=day_choices,
                                        widget=forms.CheckboxSelectMultiple,
                                        label="Available Teaching Days",
                                        required=False,
                                        disabled=True
                                        )

    lesson_show = forms.Field (
            widget=forms.TextInput,
            label="Lesson",
            required=False,
            disabled=True
    )

    class Meta:
        model = Classroom
        fields = ['lesson_show','lesson','day_selector','time','student']
        labels = {
            'time': 'Date'
        }
        widgets = {
            'student': forms.HiddenInput,
            'lesson': forms.HiddenInput,
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

class ReviewClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['state']
        widgets = {
            'state': forms.HiddenInput
        }

class UpdateReviewStudentForm(forms.ModelForm):

    rating_choices = ( ('', '----'),
                    (1, "Bad"), 
                    (2, "Poor"), 
                    (3, "Average"), 
                    (4, "Good"),
                    (5, "Excellent")
                )

    question_1 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Did the tutor start the meeting on time?"
    )

    question_2 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Was the lesson accurate to it's description?"
    )

    question_3 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Was the content interesting?"
    )

    question_4 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Was the tutor enthusiastic and engaging?"
    )

    question_5 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Would you recommend this tutor?"
    )

    tutor_rating = forms.ChoiceField (
        choices=rating_choices,
        label="Give the tutor an overall score"
    )

    rating = forms.ChoiceField (
        choices=rating_choices,
        label="Give the classroom session an overall score"
    )

    class Meta:
        model = Review
        fields = ['classroom','student_void']
        labels = {
            "student_void": "If the meeting did not take place please check this box"
        }
        widgets = {
            'classroom': forms.HiddenInput
        }

class UpdateReviewTutorForm(forms.ModelForm):

    rating_choices = ( ('', '----'),
                    (1, "Bad"), 
                    (2, "Poor"), 
                    (3, "Average"), 
                    (4, "Good"),
                    (5, "Excellent")
                )

    question_1 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Did the student attend the meeting on time?"
    )

    question_2 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Was the student enthusiastic and engaged?"
    )

    question_3 = forms.TypedChoiceField(
        coerce=lambda x: x =='True', 
        choices=((False, 'No'), (True, 'Yes')),
        label="Would you recommend this student?"
    )

    student_rating = forms.ChoiceField (
        choices=rating_choices,
        label="Give the student an overall score"
    )

    rating = forms.ChoiceField (
        choices=rating_choices,
        label="Give the classroom session an overall score"
    )

    class Meta:
        model = Review
        fields = ['classroom','tutor_void']
        labels = {
            "tutor_void": "If the meeting did not take place please check this box"
        }
        widgets = {
            'classroom': forms.HiddenInput
        }