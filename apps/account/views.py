import functools

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from openpyxl import load_workbook

from .admin import create_password
from .forms import TeacherLoginForm, PostgraduateLoginForm, GroupTeacherMemberForm
from .models import Teacher, Postgraduate, Group
from .verification import verify_teacher_by_password, verify_postgraduate_by_password

UPLOAD_XLSX_FILE = "import_data.xlsx"


def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kw):
        if request.session.has_key('user') and request.session['user']:
            return func(request, *args, **kw)
        else:
            return redirect('login')

    return wrapper


def login(request):
    """教师、研究生登陆逻辑"""
    response_data = dict()
    # 教师登陆
    if request.path == reverse('teacher_login'):
        response_data['url'] = reverse('teacher_login')
        response_data['user_type'] = '教师'
        if request.method == 'POST':
            form = TeacherLoginForm(request.POST)
            if form.is_valid():
                teacher = verify_teacher_by_password(form.cleaned_data['username'], form.cleaned_data['password'])
                if teacher:
                    request.session['type'] = 'teacher'
                    request.session['user'] = teacher.username
                    return redirect('teacher_home')
                else:
                    form.add_error(None, '密码错误')
        else:
            form = TeacherLoginForm()
        response_data['form'] = form
    # 研究生登陆
    if request.path == reverse('postgraduate_login'):
        response_data['url'] = reverse('postgraduate_login')
        response_data['user_type'] = '研究生'
        if request.method == 'POST':
            form = PostgraduateLoginForm(request.POST)
            if form.is_valid():
                postgraduate = verify_postgraduate_by_password(form.cleaned_data["pid"], form.cleaned_data['password'])
                if postgraduate:
                    request.session['type'] = 'postgraduate'
                    request.session['user'] = postgraduate.pid
                    return redirect('postgraduate_home')
                else:
                    form.add_error(None, '密码错误')
        else:
            form = PostgraduateLoginForm()
        response_data['form'] = form
    return render(request, 'account/login.html', response_data)


def logout(request):
    """教师、研究生登出逻辑"""
    try:
        del request.session['type']
        del request.session['user']
    except KeyError:
        pass
    return redirect('home')


def get_login_user(request):
    """返回已登陆的用户实例"""
    user_type = request.session.get('type')
    if user_type == 'teacher':
        username = request.session.get('user')
        return Teacher.objects.get(username=username)
    if user_type == 'postgraduate':
        pid = request.session.get('user')
        return Postgraduate.objects.get(pid=pid)


def home(request):
    """用户已登陆则跳转至对应主页"""
    login_user = get_login_user(request)
    if login_user is not None:
        if isinstance(login_user, Teacher):
            return redirect('teacher_home')
        if isinstance(login_user, Postgraduate):
            return redirect('postgraduate_home')
    return render(request, 'account/home.html')


@login_required
def teacher_home(request):
    teacher = get_login_user(request)
    return render(request, 'account/home_teacher.html', {'teacher': teacher})


@login_required
def manage_group_teacher(request):
    """组长管理组成员"""
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
    if request.method == 'POST':
        form = GroupTeacherMemberForm(data=request.POST, teacher=teacher)
        if form.is_valid():
            group = Group.objects.get(leader=teacher)
            for t in form.cleaned_data['teacher_member']:
                t.group = group
                t.save()
    else:
        form = GroupTeacherMemberForm(teacher=teacher)
    response_data['form'] = form
    return render(request, 'account/manage_group_teacher.html', response_data)


@login_required
def postgraduate_list(request):
    teacher = get_login_user(request)
    return render(request, 'account/postgraduate_list.html', {'teacher': teacher})


@login_required
def table_postgraduate_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))
        search = request.GET.get('search')
        sort_column = request.GET.get('sort')
        order = request.GET.get('order')
        teacher = get_login_user(request)
        if search:
            postgraduates = teacher.postgraduate_set.filter(Q(id=search) | Q(name=search))  # 或查询需要试用django Q
        else:
            postgraduates = teacher.postgraduate_set.all()

        if sort_column:
            sort_column = sort_column.replace('postgraduate_', '')
            if sort_column in ['id', 'name', 'teacher', 'group']:
                if order == 'desc':
                    sort_column = '-{}'.format(sort_column)
                postgraduates = postgraduates.order_by(sort_column)

        response_data = {'total': postgraduates.count(), 'rows': []}
        for postgraduate in postgraduates:
            response_data['rows'].append({
                "postgraduate_id": postgraduate.pid,
                "postgraduate_name": postgraduate.name,
                "postgraduate_teacher": postgraduate.teacher.username,
            })

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        response_data['rows'] = response_data['rows'][offset:offset + limit]
        return JsonResponse(response_data)


@login_required
def import_postgraduate_list(request):
    teacher = get_login_user(request)
    response_data = {'teacher': teacher}
    if request.method == 'POST' and request.FILES['excel']:
        excel = request.FILES['excel']
        fs = FileSystemStorage()
        fs.save(UPLOAD_XLSX_FILE, excel)  # 暂存media文件夹中
        response_data['upload_file'] = True
    elif request.method == 'GET' and request.GET.get('confirm') == 'true':
        fs = FileSystemStorage()
        workbook = load_workbook(fs.path(UPLOAD_XLSX_FILE))
        sheet_names = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(sheet_names[0])
        rows = worksheet.rows
        postgraduates = []
        for row in rows:
            line = [col.value for col in row]
            if line[0] == "学号":
                continue  # 跳过标题（TODO：以是否为数字作为判断）
            postgraduate = Postgraduate(pid=line[0],
                                        password='123456',
                                        name=line[1],
                                        teacher=teacher)
            create_password(postgraduate)
            postgraduates.append(postgraduate)
        Postgraduate.objects.bulk_create(postgraduates)
        fs.delete(UPLOAD_XLSX_FILE)  # 删除暂存文件
        return HttpResponse('OK')
    return render(request, 'account/import_postgraduate_list.html', response_data)


@login_required
def table_uploaded_postgraduate_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        fs = FileSystemStorage()
        workbook = load_workbook(fs.path(UPLOAD_XLSX_FILE))
        sheet_names = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(sheet_names[0])
        rows = worksheet.rows
        response_data = {'total': 0, 'rows': []}
        for row in rows:
            line = [col.value for col in row]
            if line[0] == "学号":
                continue
            # noinspection PyTypeChecker
            response_data['rows'].append({
                "postgraduate_id": line[0],
                "postgraduate_name": line[1],
            })

        if not offset:
            offset = 0
        if not limit:
            limit = 20
        response_data['total'] = len(response_data['rows'])
        response_data['rows'] = response_data['rows'][offset:offset + limit]
        return JsonResponse(response_data)


@login_required
def import_teacher(request):
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
    group = Group.objects.get(leader=teacher)
    if request.method == 'POST' and request.FILES['excel']:
        excel = request.FILES['excel']
        fs = FileSystemStorage()
        fs.save(UPLOAD_XLSX_FILE, excel)  # 暂存media文件夹中
        response_data['upload_file'] = True
    elif request.method == 'GET' and request.GET.get('confirm') == 'true':
        fs = FileSystemStorage()
        workbook = load_workbook(fs.path(UPLOAD_XLSX_FILE))
        sheet_names = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(sheet_names[0])
        rows = worksheet.rows
        teachers = []
        for row in rows:
            line = [col.value for col in row]
            if line[0] == "用户名":
                continue  # 跳过标题（TODO：以是否为数字作为判断）
            t = Teacher(username=line[0], password='123456', group=group)
            create_password(t)
            teachers.append(t)
        Teacher.objects.bulk_create(teachers)
        fs.delete(UPLOAD_XLSX_FILE)  # 删除暂存文件
        return HttpResponse('OK')
    return render(request, 'account/import_teacher_list.html', response_data)


@login_required
def table_uploaded_teacher_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        fs = FileSystemStorage()
        workbook = load_workbook(fs.path(UPLOAD_XLSX_FILE))
        sheet_names = workbook.get_sheet_names()
        worksheet = workbook.get_sheet_by_name(sheet_names[0])
        rows = worksheet.rows
        response_data = {'total': 0, 'rows': []}
        for row in rows:
            line = [col.value for col in row]
            if line[0] == "用户名":
                continue
            # noinspection PyTypeChecker
            response_data['rows'].append({
                "teacher_username": line[0],
            })
        if not offset:
            offset = 0
        if not limit:
            limit = 20
        response_data['total'] = len(response_data['rows'])
        response_data['rows'] = response_data['rows'][offset:offset + limit]
        return JsonResponse(response_data)


@login_required
def postgraduate_home(request):
    postgraduate = get_login_user(request)
    return render(request, 'account/home_postgraduate.html', {'postgraduate': postgraduate})
