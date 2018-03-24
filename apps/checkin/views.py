import time
from datetime import datetime

import qrcode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

from account.views import get_login_user
from .check_in_code import CheckInCode
from .models import DailyCheckIn, Computer, TempCheckInSetting, DailyCheckInSetting
from .forms import ComputerForm, TempCheckInSettingForm, DailyCheckInSettingForm


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


def temp_list(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    response_data['items'] = TempCheckInSetting.objects.filter(teacher=teacher).all()
    return render(request, 'checkin/temp_list.html', response_data)


def temp_setting(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    if request.method == 'POST':
        form = TempCheckInSettingForm(request.POST)
        if form.is_valid():
            setting = form.save(commit=False)
            setting.teacher = teacher
            setting.save()
            return redirect('check_in_temp_list')
        else:
            print(form.errors)
    else:
        form = TempCheckInSettingForm()
    response_data['form'] = form
    return render(request, 'checkin/temp_setting.html', response_data)


def daily_setting(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    instance = None
    if DailyCheckInSetting.objects.filter(teacher=teacher).exists():
        instance = DailyCheckInSetting.objects.filter(teacher=teacher).first()
    if request.method == 'POST':
        form = DailyCheckInSettingForm(request.POST, instance=instance)
        if form.is_valid():
            setting = form.save(commit=False)
            setting.teacher = teacher
            setting.save()
    else:
        form = DailyCheckInSettingForm(instance=instance)
    response_data['form'] = form
    return render(request, 'checkin/daily_setting.html', response_data)


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
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    if request.method == 'GET':
        date = request.GET.get('date')
        if date is not None:
            # 处理图表显示数据
            json_data = {}
            if date == 'today':
                date = datetime.today()
            json_data['startDate'] = date.strftime("%Y-%m-%d")
            check_in_set = DailyCheckIn.objects.filter(date=date, postgraduate__teacher=teacher).all()
            setting = DailyCheckInSetting.objects.get(teacher=teacher)  # 读取日常签到设置
            json_data['times'] = setting.times
            for i in range(setting.times):
                index = i + 1
                start = 'time{}_start'.format(index)
                end = 'time{}_end'.format(index)
                json_data[start] = to_js_date(date, getattr(setting, start))
                json_data[end] = to_js_date(date, getattr(setting, end))
            json_data['data'] = []
            for record in check_in_set:
                json_data['data'].append({
                    'name': record.postgraduate.name,
                    'check1': to_js_date(record.date, record.check1),
                    'check2': to_js_date(record.date, record.check2),
                    'check3': to_js_date(record.date, record.check3),
                    'check4': to_js_date(record.date, record.check4)
                })
            return JsonResponse(json_data)
        else:
            return render(request, 'checkin/show_check_in.html', response_data)


def to_js_date(d, t):
    if not t:
        return None
    dt = datetime.combine(d, t)
    return int(time.mktime(dt.timetuple())) * 1000
