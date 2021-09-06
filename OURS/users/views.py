from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .forms import ProfileForm, UserForm

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

@login_required
def get_profile(req, id):
    user = User.objects.get(id=id)
    context = {"user":user}
    return render(req,'auth/single-profile.html',context)

@login_required
@transaction.atomic
def update_profile(req):
    if req.method == 'POST':
        user_form = UserForm(req.POST, instance=req.user)
        profile_form = ProfileForm(req.POST, req.FILES, instance=req.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(req, 'Your profile was successfully updated!')
            return redirect('update_profile')
        else:
            messages.error(req, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=req.user)
        profile_form = ProfileForm(instance=req.user.profile)
    return render(req, 'auth/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
# def log_in(req):
#     return redirect('dashboard')