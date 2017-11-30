from django.shortcuts import render, redirect
from django.urls import reverse

from management.forms import TeacherLoginForm, PostgraduateLoginForm
from management.models import Teacher, Postgraduate


def home(request):
    """用户已登陆则跳转至对应主页"""
    login_user = __get_login_user(request)
    if login_user is not None:
        if isinstance(login_user, Teacher):
            return redirect('teacher_home')
        if isinstance(login_user, Postgraduate):
            return redirect('postgraduate_home')
    return render(request, 'home.html')


def choose_login_type(request):
    return render(request, 'choose_login_type.html')


def logout(request):
    try:
        del request.session['type']
        del request.session['user']
    except KeyError:
        pass
    return redirect('home')


def login(request):
    """教师、研究生登陆逻辑"""
    data = {}
    # 教师登陆
    if request.path == reverse('teacher_login'):
        data['url'] = reverse('teacher_login')
        data['user_type'] = '教师'
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
                    return redirect('teacher_home')
        data['form'] = form
    # 研究生登陆
    if request.path == reverse('postgraduate_login'):
        data['url'] = reverse('postgraduate_login')
        data['user_type'] = '研究生'
        if request.method == 'GET':
            form = PostgraduateLoginForm()
        else:
            form = PostgraduateLoginForm(request.POST)
            if form.is_valid():
                _id = request.POST.get('id', '')
                password = request.POST.get('password', '')
                postgraduate = Postgraduate.objects.get(id=_id)
                if postgraduate.password == password:
                    request.session['type'] = 'postgraduate'
                    request.session['user'] = postgraduate.id
                    return redirect('postgraduate_home')
        data['form'] = form
    return render(request, 'login.html', data)


def teacher_home(request):
    teacher = __get_login_user(request)
    return render(request, 'home_teacher.html', {'teacher': teacher})


def postgraduate_home(request):
    postgraduate = __get_login_user(request)
    return render(request, 'home_postgraduate.html', {'postgraduate': postgraduate})


def __get_login_user(request):
    """返回已登陆的用户实例"""
    user_type = request.session.get('type')
    if user_type == 'teacher':
        username = request.session.get('user')
        return Teacher.objects.get(username=username)
    if user_type == 'postgraduate':
        _id = request.session.get('user')
        return Postgraduate.objects.get(id=_id)
