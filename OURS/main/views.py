from django.core import paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Classroom, Lesson, Category, Skill, SkillLevels, SkillLevels
from .forms import FinaliseClassroomForm, NewClassroomForm, NewLessonForm, ReviewClassroomForm, UpdateClassroomForm
from datetime import datetime

# Create your views here.

def homepage(req):
    return render(req, 'pages/homepage.html')

@login_required
def dashboard(req):
    # Only bring in the 5 most recent lessons
    lessons = Lesson.objects.order_by('-created')[:5]
    student_classrooms = Classroom.objects.filter(student=req.user)[:5]
    tutor_classrooms = Classroom.objects.filter(lesson__tutor=req.user)[:5]
    context = {
        "lessons": lessons,
        "student_rooms": student_classrooms,
        "tutor_rooms": tutor_classrooms
    }

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
    
    filter = req.GET.get('filter')
    value = req.GET.get('value')
    if filter == 'title':
        lessons = Lesson.objects.filter(title__icontains=value).order_by('-created')
    elif filter == 'level':
        lessons = Lesson.objects.filter(skill_level=value[0].upper()).order_by('-created')
    elif filter == 'skill':
        lessons = Lesson.objects.filter(skill__name__icontains=value).order_by('-created')
    elif filter == 'category':
        lessons = Lesson.objects.filter(skill__category__name__icontains=value).order_by('-created')
    elif filter == 'tutor':
        lessons = Lesson.objects.filter(tutor__username__icontains=value).order_by('-created')
    elif filter == 'rating':
        lessons = Lesson.objects.filter(tutor__profile__rating=value).order_by('-created')
    else:
        lessons = Lesson.objects.filter().order_by('-created')

    catagories = Category.objects.all()

    # the bellow argument is how many items will be on a page
    paginator = Paginator(lessons, 5)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if filter:
        filter = filter.capitalize()

    context = {
        "page_obj": page_obj, 
        "catagories": catagories,
        "filter": filter,
        "filterText": value
    }

    return render(req, 'pages/find-a-lesson.html', context)

@login_required
def update_a_lesson(req, id):
    if req.method == 'POST':
        updated_lesson = NewLessonForm(req.POST)
        if updated_lesson.is_valid():
            lesson = get_object_or_404(Lesson, pk=id)
            lesson.skill = updated_lesson.cleaned_data['skill']
            lesson.skill_level = updated_lesson.cleaned_data['skill_level']
            lesson.title = updated_lesson.cleaned_data['title']
            lesson.description = updated_lesson.cleaned_data['description']
            lesson.days = updated_lesson.cleaned_data['day_selector']
            lesson.save()
            return redirect('lesson-single', id=lesson.id)

    # return the form with the data already filled in
    lesson = get_object_or_404(Lesson, pk=id)
    selectedDays = lesson.days.replace('[','')
    selectedDays = selectedDays.replace(']','')
    selectedDays = selectedDays.replace(' ','')
    selectedDays = selectedDays.replace('\'','')
    selectedDays = selectedDays.split(',')
    form = NewLessonForm(initial={ 
        'tutor': lesson.tutor , 
        'skill': lesson.skill, 
        'title': lesson.title, 
        'description': lesson.description, 
        'days': lesson.days,
        'day_selector': selectedDays
    })
    return render(req, 'pages/update-lesson.html', {"form": form, "id": id})

@login_required
def delete_a_lesson(req, id):
    lesson = get_object_or_404(Lesson, pk=id)
    lesson.delete()
    return redirect('find-a-lesson')

@login_required
def classroom_create(req, id):

    if req.method == 'POST':
        form = NewClassroomForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            context = {
                "form": form,
            }
            return render(req, 'pages/classroom-create.html', context )

    lesson = get_object_or_404(Lesson, pk=id)
    selectedDays = lesson.days.replace('[','')
    selectedDays = selectedDays.replace(']','')
    selectedDays = selectedDays.replace(' ','')
    selectedDays = selectedDays.replace('\'','')
    selectedDays = selectedDays.split(',')

    form = NewClassroomForm(initial={
        'lesson': lesson,
        'student': req.user,
        'day_selector': selectedDays
    })
    context = {
        "form": form
    }
    return render(req, 'pages/classroom-create.html', context )

@login_required
def classroom_detail(req,id):
    single_classroom = get_object_or_404(Classroom, pk=id)
    context = {
        "user": req.user,
        "classroom": single_classroom
    }
    return render(req, 'pages/classroom-single.html', context)

@login_required
def classroom_update(req,id):

    single_classroom = get_object_or_404(Classroom, pk=id)
    if req.method == 'POST':
        getCopy = req.POST.copy()
        newDatetime = getCopy['date'] + ' ' + getCopy['time']
        newDatetime = datetime.strptime(newDatetime, '%Y-%m-%d %H:%M')
        getCopy['time'] = newDatetime
        form = UpdateClassroomForm(getCopy)
        if form.is_valid():
            single_classroom.time = form.cleaned_data['time']
            single_classroom.state = "AC"
            single_classroom.save()
            return redirect('classroom-single', id=single_classroom.id)
        else:
            print(form.errors)

    form = UpdateClassroomForm(initial={
        "date" : single_classroom.time.date(),
        "time" : single_classroom.time.time(),
        "state": single_classroom.state
    })
    context = {
        "form": form
    }
    return render(req, 'pages/classroom-update.html', context)

@login_required
def classroom_confirm(req,id):
    classroom = get_object_or_404(Classroom, pk=id)
    classroom.state = 'CF'
    classroom.save()
    return redirect('classroom-single', id=classroom.id)

@login_required
def classroom_finalise(req,id):
    if req.method == 'POST':
        form = FinaliseClassroomForm(req.POST)
        if form.is_valid():
            classroom = get_object_or_404(Classroom, pk=id)
            classroom.state = 'UP'
            classroom.room_details = form.cleaned_data['room_details']
            classroom.save()
            return redirect('classroom-single', id=classroom.id)
        else:
            print(form.errors)    
    classroom = get_object_or_404(Classroom, pk=id)
    form = FinaliseClassroomForm()
    context = {
        "form": form 
    }
    return render(req, 'pages/classroom-update-tutor.html', context)

@login_required
def classroom_review(req,id):
    classroom = get_object_or_404(Classroom, pk=id)
    form = ReviewClassroomForm(initial={
        'state': classroom.state
    })
    context = {
        "form": form 
    }
    return render(req, 'pages/classroom-review.html', context)

