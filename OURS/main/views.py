from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Lesson
from .forms import NewLessonForm

# Create your views here.

def homepage(req):
    return render(req, 'pages/homepage.html')

@login_required
def dashboard(req):
    # Only bring in the 5 most recent lessons
    lessons = Lesson.objects.order_by('-created')[:5]
    context = {"lessons": lessons}

    return render(req, 'pages/dashboard.html', context)

@login_required
def lesson_create(req):
    if req.method == 'POST':
        if req.user.is_authenticated:
            form = NewLessonForm(req.POST)
            if form.is_valid():
                form.instance.days = form.cleaned_data['day_selector']
                new_lesson = form.save()
                return redirect('lesson-single', id=new_lesson.id)
    else:
        form = NewLessonForm(initial={ 'tutor': req.user })
        context = {"form":form}
        return render(req, 'pages/lesson-create.html',context)

@login_required
def lesson_detail_page(req,id):
    single_lesson = get_object_or_404(Lesson, pk=id)
    context = {"lesson":single_lesson}
    return render(req, 'pages/lesson-single.html', context)