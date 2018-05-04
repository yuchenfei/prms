from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.models import Postgraduate, Group
from account.views import get_login_user
from leave.models import Leave


def ask_for_leave(request):
    postgraduate = get_login_user(request)
    response = dict(postgraduate=postgraduate)
    if request.method == 'POST':
        date = request.POST.get('date')
        excuse = request.POST.get('excuse')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        if not Leave.objects.filter(postgraduate=postgraduate, date=date).exists():
            Leave.objects.create(
                postgraduate=postgraduate,
                date=date,
                excuse=excuse,
                time_of_submission=datetime.now()
            )
            return redirect('leave_list_p')
        else:
            # 当日已请过假
            messages.add_message(request, messages.WARNING, '{} 已请过假期'.format(date))
    return render(request, 'leave/ask_for_leave.html', response)


def list_list_p(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')
        postgraduate = get_login_user(request)
        response = dict(postgraduate=postgraduate)
        leave_query = Leave.objects.filter(postgraduate=postgraduate)
        leave_query = leave_query.order_by('-time_of_submission')
        paginator = Paginator(leave_query, 5)
        try:
            leave_list = paginator.page(int(page))
        except PageNotAnInteger:
            leave_list = paginator.page(1)
            page = 1
        except EmptyPage:
            leave_list = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        response['leave_list'] = leave_list
        response['range'] = paginator.page_range
        response['page'] = int(page)
        return render(request, 'leave/leave_list_p.html', response)


def leave_list_t(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')
        teacher = get_login_user(request)
        response = dict(teacher=teacher)
        # 组长获取课题组所有研究生，普通教师获取自己的研究生
        if teacher.is_leader:
            group = Group.objects.get(leader=teacher)
            postgraduates = Postgraduate.objects.filter(Q(teacher=teacher) | Q(teacher__group=group))
        else:
            postgraduates = Postgraduate.objects.filter(teacher=teacher)
        # 是否显示已处理的记录
        leave_query = Leave.objects.filter(postgraduate__in=postgraduates)
        leave_query = leave_query.order_by('-time_of_submission')
        paginator = Paginator(leave_query, 5)
        try:
            leave_list = paginator.page(int(page))
        except PageNotAnInteger:
            leave_list = paginator.page(1)
            page = 1
        except EmptyPage:
            leave_list = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        response['leave_list'] = leave_list
        response['range'] = paginator.page_range
        response['page'] = int(page)
        return render(request, 'leave/leave_list_t.html', response)


def processes_leave(request, leave_id):
    print(request.get_raw_uri())
    teacher = get_login_user(request)
    if request.method == 'POST':
        leave = Leave.objects.get(id=leave_id)
        result = request.POST.get('result')
        if result == 'approve':
            leave.approve(teacher)
        elif result == 'reject':
            leave.reject(teacher)
    return redirect('leave_list_t')
