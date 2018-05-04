import time
from datetime import datetime, timedelta
from operator import itemgetter

import qrcode
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

from account.models import Postgraduate
from account.views import get_login_user, login_required
from leave.models import Leave
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
    if request.method == 'GET':
        response_data = dict()
        response_data['teacher'] = teacher = get_login_user(request)
        page = request.GET.get('page', '1')
        if teacher.group:
            items = TempCheckInSetting.objects.filter(
                Q(teacher=teacher) | Q(teacher__group=teacher.group, is_group=True)).order_by('-date', '-time').all()
        else:
            items = TempCheckInSetting.objects.filter(teacher=teacher).order_by('-date', '-time').all()
        paginator = Paginator(items, 5)
        try:
            items_p = paginator.page(int(page))
        except PageNotAnInteger:
            items_p = paginator.page(1)
            page = 1
        except EmptyPage:
            items_p = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        response_data['items'] = items_p
        response_data['range'] = paginator.page_range
        response_data['page'] = int(page)
        return render(request, 'checkin/temp_list.html', response_data)


def temp_new(request):
    response_data = dict()
    teacher = get_login_user(request)
    response_data['teacher'] = teacher
    if request.method == 'POST':
        form = TempCheckInSettingForm(request.POST)
        if form.is_valid():
            setting = form.save(commit=False)
            setting.teacher = teacher
            setting.save()
            form.save_m2m()
            return redirect('check_in_temp_list')
        else:
            print(form.errors)
    else:
        form = TempCheckInSettingForm()
    response_data['form'] = form
    return render(request, 'checkin/temp_setting.html', response_data)


def temp_delete(request, temp_id):
    temp_setting = TempCheckInSetting.objects.get(id=temp_id)
    if temp_setting:
        name = temp_setting.name
        temp_setting.delete()
        messages.add_message(request, messages.INFO, '成功删除 {}'.format(name))
    return redirect('check_in_temp_list')


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
            form.save_m2m()
    else:
        form = DailyCheckInSettingForm(instance=instance)
    response_data['form'] = form
    return render(request, 'checkin/daily_setting.html', response_data)


def computer_list(request):
    if request.method == 'GET':
        teacher = get_login_user(request)
        response = dict(teacher=teacher)
        if request.GET.get('table'):
            limit = int(request.GET.get('limit'))
            offset = int(request.GET.get('offset'))
            search = request.GET.get('search')
            sort_column = request.GET.get('sort')
            order = request.GET.get('order')
            computers = Computer.objects.filter(teacher=teacher)
            if search:
                computers = computers.filter(name__icontains=search)
            if sort_column:
                sort_column = sort_column.replace('computer_', '')
                if sort_column in ['name']:
                    if order == 'desc':
                        sort_column = '-{}'.format(sort_column)
                    computers = computers.order_by(sort_column)
            total = computers.count()
            rows = list()
            for computer in computers:
                rows.append({
                    'computer_name': computer.name,
                    'computer_cpu_id': computer.cpu_id
                })
            rows = rows[offset:offset + limit]
            return JsonResponse(dict(total=total, rows=rows))
        return render(request, 'checkin/computer_list.html', response)


def computer_new(request):
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            computer = form.save(commit=False)
            computer.teacher = teacher
            computer.save()
            return redirect('computer_list')
    else:
        form = ComputerForm()
    response_data['form'] = form
    return render(request, 'checkin/computer_new.html', response_data)


@csrf_exempt
@login_required
def computer_delete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher = get_login_user(request)
        if name:
            Computer.objects.get(teacher=teacher, name=name).delete()
            return JsonResponse({'result': True})


def show_check_in(request):
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
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


def check_in_status(request):
    if request.method == 'GET':
        response = dict()
        response['teacher'] = teacher = get_login_user(request)

        date_range = request.GET.get('date_range')
        if date_range:  # 获取图标数据
            # 解析需要显示的时间范围
            try:
                date_range = date_range.split(' to ')
                begin_date = datetime.strptime(date_range[0], '%Y-%m-%d')
                end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
            except Exception as e:
                print(e)
                begin_date = end_date = datetime.today()
            date_range = [begin_date, end_date]
            print(date_range)
            # 查询数据
            setting = DailyCheckInSetting.objects.get(teacher=teacher)  # 日常签到设置
            postgraduates = Postgraduate.objects.filter(teacher=teacher).all()  # 所有研究生
            check_in_set = DailyCheckIn.objects.filter(date__range=date_range,
                                                       postgraduate__teacher=teacher).all()  # 签到记录
            leave_set = Leave.objects.filter(date__range=date_range,
                                             postgraduate__teacher=teacher,
                                             state=True).all()  # 请假记录
            # 计算应签到的次数
            days = 0
            d = begin_date
            delta = timedelta(days=1)
            while d < end_date:
                if str(d.weekday()) in setting.week_option:
                    days += 1
                d += delta
            today_times = 0
            if str(end_date.weekday()) in setting.week_option:  # 单独判断最后一天的情况
                today = datetime.today()
                if end_date.date() == today.date():
                    # 今日需判断签到时间是否已过
                    for i in range(setting.times):
                        if getattr(setting, 'time{}_end'.format(i + 1)) < today.time():
                            today_times += 1
                else:
                    days += 1
            total = setting.times * days + today_times
            # 处理签到记录
            check_in_times = dict()
            for record in check_in_set:
                name = record.postgraduate.name
                times = 0
                for i in range(4):
                    if getattr(record, 'check{}'.format(i + 1)):
                        times += 1
                check_in_times[name] = min(times, setting.times) + check_in_times.setdefault(name, 0)
            # 处理请假记录
            leave_times = dict()
            for record in leave_set:
                name = record.postgraduate.name
                leave_times[name] = setting.times + leave_times.setdefault(name, 0)
            # 数据汇总
            data = []
            if total > 0:
                for postgraduate in postgraduates:
                    name = postgraduate.name
                    cit = check_in_times.get(name, 0)
                    lt = leave_times.get(name, 0)
                    data.append({
                        'name': name,
                        'check_in': cit,
                        'leave': lt,
                        'absenteeism': total - cit - lt
                    })
                data = sorted(data, key=itemgetter('check_in'), reverse=True)  # 按照签到次数降序排序
            return JsonResponse(dict(data=data))
        else:
            try:
                response['setting'] = DailyCheckInSetting.objects.get(teacher=teacher)  # 日常签到设置
            except ObjectDoesNotExist:
                # 教师未设置日常签到
                return redirect('check_in_daily_setting')
            today = datetime.today()
            response['start'] = today - timedelta(today.weekday()) if today.weekday() != 0 else today
            return render(request, 'checkin/status.html', response)


def my_items(request):
    if request.method == 'GET':
        response_data = dict()
        response_data['postgraduate'] = postgraduate = get_login_user(request)
        page = request.GET.get('page', '1')
        response_data['daily_setting'] = None
        if DailyCheckInSetting.objects.filter(teacher=postgraduate.teacher).exists():
            response_data['daily_setting'] = setting = DailyCheckInSetting.objects.get(teacher=postgraduate.teacher)
            week_str = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            response_data['week_option'] = []
            for i in range(7):
                if str(i) in list(setting.week_option):
                    response_data['week_option'].append(week_str[i])
        items = TempCheckInSetting.objects.filter(teacher=postgraduate.teacher).order_by('-date', '-time').all()
        paginator = Paginator(items, 5)
        try:
            items_p = paginator.page(int(page))
        except PageNotAnInteger:
            items_p = paginator.page(1)
            page = 1
        except EmptyPage:
            items_p = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        response_data['items'] = items_p
        response_data['range'] = paginator.page_range
        response_data['page'] = int(page)
        return render(request, 'checkin/my_items.html', response_data)


def to_js_date(d, t):
    if not t:
        return None
    dt = datetime.combine(d, t)
    return int(time.mktime(dt.timetuple())) * 1000
