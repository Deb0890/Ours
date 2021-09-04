from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login

# Create your views here.

def sign_up(req):
    if req.method == "POST":
        new_user = forms.UserSignupForm(req.POST)
        if new_user.is_valid():
            new_user.save()
            new_user_login_details = authenticate(username=new_user.cleaned_data['username'], password=new_user.cleaned_data['password1'])
            login(req, new_user_login_details)
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