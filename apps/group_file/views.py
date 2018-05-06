from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Teacher
from account.views import get_login_user, login_required
from .forms import GroupFileForm
from .models import GroupFile


@login_required
def group_file_list(request):
    if request.method == 'GET':
        response_data = dict()
        user = get_login_user(request)
        # 判断用户类型
        if isinstance(user, Teacher):
            response_data['teacher'] = teacher = user
        else:
            response_data['postgraduate'] = user
        # 表格显示相关逻辑
        if request.GET.get('table'):
            limit = int(request.GET.get('limit'))
            offset = int(request.GET.get('offset'))
            search = request.GET.get('search')
            sort_column = request.GET.get('sort')
            order = request.GET.get('order')
            if isinstance(user, Teacher):
                group_files = GroupFile.objects.filter(group=user.group)
            else:
                group_files = GroupFile.objects.filter(group=user.teacher.group, show=True)
            if search:
                group_files = group_files.filter(Q(title__icontains=search) | Q(owner__name__icontains=search))
            if sort_column:
                sort_column = sort_column.replace('group_file_', '')
                if sort_column in ['title', 'owner', 'date', 'show']:
                    if order == 'desc':
                        sort_column = '-{}'.format(sort_column)
                    group_files = group_files.order_by(sort_column)
            json = {'total': group_files.count(), 'rows': []}
            for group_file in group_files:
                is_owner = False
                if teacher:
                    if teacher == group_file.owner:
                        is_owner = True
                json['rows'].append({
                    'group_file_title': group_file.title,
                    'group_file_describe': group_file.describe,
                    'group_file_show': '是' if group_file.show else '否',
                    'group_file_owner': group_file.owner.name,
                    'group_file_date': group_file.date.strftime('%Y/%m/%d %H:%M'),
                    'is_owner': is_owner,
                    'file_url': group_file.file.url
                })
            json['rows'] = json['rows'][offset:offset + limit]
            return JsonResponse(json)
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


@csrf_exempt
@login_required
def group_file_delete(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            GroupFile.objects.get(title=title).delete()
            return JsonResponse({'result': True})
