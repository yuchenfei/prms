from datetime import datetime

import qrcode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

from account.views import get_login_user
from .check_in_code import CheckInCode
from .models import DailyCheckIn, Computer, CheckInSetting
from .forms import ComputerForm, CheckInSettingForm


@csrf_exempt
def check_in(request):
    if request.method == 'POST':
        cpu_id = request.POST.get('cpu_id', None)
        code, is_valid = CheckInCode(cpu_id=cpu_id).get_code()

        buf = BytesIO()
        img = qrcode.make(code)
        img.save(buf)
        return HttpResponse(buf.getvalue(), content_type="image/png")
    else:
        return render(request, 'checkin/check_in.html')


def setting(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    if request.method == 'POST':
        form = CheckInSettingForm(request.POST)
        if form.is_valid():
            check_in_setting = form.save(commit=False)
            check_in_setting.teacher = teacher
            check_in_setting.c_type = 2
            check_in_setting.save()
            redirect('check_in_setting')
        else:
            print(form.errors)
    else:
        form = CheckInSettingForm()
    response_data['form'] = form
    response_data['items'] = CheckInSetting.objects.filter(teacher=teacher,
                                                           c_type=CheckInSetting.TYPE_CHOICES[1][0]).all()
    return render(request, 'checkin/check_in_setting.html', response_data)


def computer_list(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    response_data['computer_list'] = Computer.objects.all()
    return render(request, 'checkin/computer_list.html', response_data)


def computer_add(request):
    teacher = get_login_user(request)
    response_data = {'teacher': teacher}
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('computer_list')
    else:
        form = ComputerForm()
    response_data['form'] = form
    return render(request, 'checkin/computer_add.html', response_data)


def show_check_in(request):
    teacher = get_login_user(request)
    response_data = {'teacher': teacher}
    if request.method == 'GET':
        date = request.GET.get('date')
        if date is not None:
            json_data = {}
            if date == 'today':
                date = datetime.now().date()
                json_data['startDate'] = date.strftime("%Y-%m-%d")
            check_in_set = DailyCheckIn.objects.filter(date=date).filter(postgraduate__teacher=teacher).all()
            json_data['data'] = []
            for record in check_in_set:
                json_data['data'].append(
                    {
                        'name': record.postgraduate.name,
                        'forenoon_in': to_js_date(record.date, record.forenoon_in),
                        'forenoon_out': to_js_date(record.date, record.forenoon_out),
                        'afternoon_in': to_js_date(record.date, record.afternoon_in),
                        'afternoon_out': to_js_date(record.date, record.afternoon_out)
                    }
                )
            return JsonResponse(json_data)
        else:
            return render(request, 'checkin/show_check_in.html', response_data)


def to_js_date(d, t):
    dt = datetime.combine(d, t)
    return int(datetime.time.mktime(dt.timetuple())) * 1000
