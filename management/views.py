from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from management.forms import TeacherLoginForm, PostgraduateLoginForm
from management.models import Teacher


def home(request):
    return redirect('/management/choose_login_type')


def choose_login_type(request):
    return render(request, 'choose_login_type.html')


def login(request):
    data = {}
    if request.path == reverse('teacher_login'):
        data['url'] = reverse('teacher_login')
        data['type'] = '教师'
        if request.method == 'GET':
            form = TeacherLoginForm()
        else:
            form = TeacherLoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                teacher = Teacher.objects.get(username=username)
                if teacher.password == password:
                    request.session['type'] = 'teacher'
                    request.session['user'] = teacher.username
                    return redirect(reverse('teacher_home'))
        data['form'] = form

    if request.path == reverse('postgraduate_login'):
        data['url'] = reverse('teacher_login')
        data['type'] = '研究生'
        if request.method == 'GET':
            form = PostgraduateLoginForm()
        else:
            form = PostgraduateLoginForm(request.POST)
        data['form'] = form

    return render(request, 'login.html', data)


def teacher_home(request):
    return HttpResponse('hello teacher')
