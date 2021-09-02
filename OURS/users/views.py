from django.shortcuts import render, redirect
from . import forms

# Create your views here.

def sign_up(req):
    if req.method == "POST":
        new_user = forms.UserSignupForm(req.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('log_in')
    else:
        form = forms.UserSignupForm()
        context = {"form": form}
        return render(req, 'auth/signup.html', context)


def log_in(req):
    return