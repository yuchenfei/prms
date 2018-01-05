from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from account.views import __get_login_user
from leave.models import Leave


def ask_for_leave(request):
    postgraduate = __get_login_user(request)
    response_data = {'postgraduate': postgraduate}
    if request.method == 'POST':
        date = request.POST.get('date')
        excuse = request.POST.get('excuse')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        # TODO:是否重复
        Leave.objects.create(
            postgraduate=postgraduate,
            date=date,
            excuse=excuse,
            time_of_submission=datetime.now()
        )
        return HttpResponse('提交成功！')
    return render(request, 'leave/ask_for_leave.html', response_data)


def leave_list(request):
    teacher = __get_login_user(request)
    response_data = {'teacher': teacher}
    postgraduates = teacher.postgraduate_set.all()
    leaves = Leave.objects.filter(state=None).all()
    leave_set = set()
    for leave in leaves:
        if leave.postgraduate in postgraduates:
            leave_set.add(leave)
    response_data['leave_set'] = leave_set
    return render(request, 'leave/leave_list.html', response_data)
