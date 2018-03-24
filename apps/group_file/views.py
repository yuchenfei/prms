from datetime import datetime
from django.shortcuts import render, redirect

from account.models import Teacher
from account.views import get_login_user, login_required
from .forms import GroupFileForm
from .models import GroupFile


@login_required
def group_file_list(request):
    # todo:完善不同用户的显示逻辑
    response_data = dict()
    user = get_login_user(request)
    if isinstance(user, Teacher):
        response_data['teacher'] = user
        group = user.group
    else:
        response_data['postgraduate'] = user
        group = user.teacher.group
    response_data['file_list'] = GroupFile.objects.filter(group=group).all()
    return render(request, 'group_file/group_file_list.html', response_data)


@login_required
def group_file_upload(request):
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
    if request.method == 'POST':
        form = GroupFileForm(request.POST, request.FILES)
        if form.is_valid():
            group_file = form.save(commit=False)
            group_file.group = teacher.group
            group_file.owner = teacher
            group_file.date = datetime.now()
            group_file.save()
            return redirect('group_file_list')
    else:
        form = GroupFileForm()
    response_data['form'] = form
    return render(request, 'group_file/group_file_upload.html', response_data)
