from django.shortcuts import render, redirect
from . import forms

# Create your views here.

def sign_up(req):
    if req.method == "POST":
        new_user = forms.UserSignupForm(req.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('dashboard')
        else:
            print(new_user.errors)
            form = forms.UserSignupForm()
            context = {"form": form, "errors": new_user.errors}
            return render(req, 'auth/signup.html', context)

    else:
        form = forms.UserSignupForm()
        context = {"form": form}
        return render(req, 'auth/signup.html', context)


# def log_in(req):
#     return redirect('dashboard')