import hashlib
import random
from datetime import datetime
from os import urandom

import qrcode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from io import BytesIO

from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from account.views import get_login_user
from .models import CheckIn, Computer
from .forms import ComputerForm


@csrf_exempt
def check_in(request):
    if request.method == 'POST':
        cpu_id = request.POST.get('cpu_id', '')

        code = cache.get('qr_code', None)
        if not code:
            if cpu_id:
                c = Computer.objects.get(cpu_id=cpu_id)
                m = hashlib.sha256()
                m.update(cpu_id.encode('utf-8'))
                code = urandom(32).hex() + m.hexdigest() + str(c.id)
            else:
                code = urandom(64).hex()
            print(code)
            cache.set('qr_code', code, 30)

        buf = BytesIO()
        img = qrcode.make(code)
        img.save(buf)
        return HttpResponse(buf.getvalue(), content_type="image/png")
    else:
        return render(request, 'checkin/check_in.html')

    # else:
    #     pass
    # postgraduate = Postgraduate.objects.get(id=request.POST.get('postgraduate'))
    # records = CheckIn.objects.filter(date=datetime.now().date(), postgraduate=postgraduate)
    # if records:
    #     record = records[0]
    #     changed = False
    #     current_time = datetime.now().time()
    #     if record.forenoon_out is None:
    #         record.forenoon_out = current_time
    #         changed = True
    #     elif record.afternoon_in is None:
    #         record.afternoon_in = current_time
    #         changed = True
    #     elif record.afternoon_out is None:
    #         record.afternoon_out = current_time
    #         changed = True
    #     if changed:
    #         record.save()
    #         return redirect('check_in')
    #     else:
    #         return HttpResponse('今日签到已完成！')
    # else:
    #     record = CheckIn.objects.create(postgraduate=postgraduate, date=datetime.now().date())
    # record.forenoon_in = datetime.now().time()
    # record.save()
    # return redirect('check_in')


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
            check_in_set = CheckIn.objects.filter(date=date).filter(postgraduate__teacher=teacher).all()
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
