from django.shortcuts import render
from . import forms

# Create your views here.

def sign_up(req):
    form = forms.UserSignupForm()
    context = {"form": form}
    return render(req, 'auth/signup.html', context)


def log_in(req):
    return