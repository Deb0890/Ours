from django import forms
from .models import Skill

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name','category']