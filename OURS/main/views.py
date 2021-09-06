from django.core import paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Lesson, Category, Skill, SkillLevels, SkillLevels
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
    days = ["mon","tue","wed","thu","fri","sat","sun"]
    context = {"lesson":single_lesson, "user": req.user.id, "days": days}
    return render(req, 'pages/lesson-single.html', context)

@login_required
def find_a_lesson(req):
    
    lessons = Lesson.objects.order_by('-created')
    catagories = Category.objects.all()
    
    # the bellow argument is how many items will be on a page
    paginator = Paginator(lessons, 5)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {"page_obj": page_obj, "catagories": catagories}
    return render(req, 'pages/find-a-lesson.html', context)
