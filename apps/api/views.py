import base64

import jwt
import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.verification import verify_postgraduate_by_password, verify_postgraduate_by_jwt
from checkin.models import DailyCheckInSetting, DailyCheckIn, TempCheckInSetting, TempCheckIn, Computer
from checkin.check_in_code import CheckInCode
from .models import Device


@csrf_exempt
def auth(request):
    """认证用户身份"""
    if request.method == 'POST':
        json = {'result': False,
                'token': '',
                'reason': 0}
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        imei = request.POST.get('imei')

        # 解密数据
        phone = decrypt_data(phone)
        password = decrypt_data(password)
        imei = decrypt_data(imei)

        postgraduate = verify_postgraduate_by_password(phone, password)
        if postgraduate:
            if not Device.objects.filter(postgraduate=postgraduate).exists():
                Device.objects.create(postgraduate=postgraduate, imei=imei)
            else:
                if not postgraduate.device.imei:
                    postgraduate.device.imei = imei
                    postgraduate.device.save()
                elif postgraduate.device.imei != imei:
                    json['reason'] = 1
                    return JsonResponse(json)
            payload = {
                'iat': int(time.time()),  # 签发时间
                'exp': int(time.time()) + 86400 * 7,  # 过期时间
                'sub': str(postgraduate.phone),
                'name': str(postgraduate.name)
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            json['result'] = True
            json['token'] = token.decode()
        else:
            json['reason'] = 0
        return JsonResponse(json)


@csrf_exempt
def items(request):
    """获取签到项目及其状态"""
    json = {
        'auth_result': False,
        'daily_times': 1,
        'daily_time_interval': '',
        'daily_ok': [],
        'temp_id': [],
        'temp_name': [],
        'temp_time': [],
        'temp_time_interval': [],
        'temp_ok': []
    }
    if request.method == 'POST':
        token = request.POST.get('token')
        postgraduate = verify_postgraduate_by_jwt(token)
        if postgraduate:
            json['auth_result'] = True
            # 日常签到相关
            if DailyCheckInSetting.objects.filter(teacher=postgraduate.teacher).exists():
                daily_setting = DailyCheckInSetting.objects.get(teacher=postgraduate.teacher)
                times = daily_setting.times
                json['daily_times'] = times
                for i in range(times):
                    index = i + 1
                    start = 'time{}_start'.format(index)
                    end = 'time{}_end'.format(index)
                    json['daily_time_interval'] += getattr(daily_setting, start).strftime('%H:%M')
                    json['daily_time_interval'] += '-'
                    json['daily_time_interval'] += getattr(daily_setting, end).strftime('%H:%M')
                    json['daily_time_interval'] += ';'
                today_check_in = DailyCheckIn.objects.filter(date=datetime.today(), postgraduate=postgraduate)
                if today_check_in.exists():
                    for i in range(times):
                        index = i + 1
                        if getattr(today_check_in[0], 'check{}'.format(index)):
                            json['daily_ok'].append(index)
            else:
                json['daily_times'] = 0
            # 临时签到相关
            if postgraduate.teacher.group:
                q1 = Q(teacher=postgraduate.teacher, date=datetime.today())
                q2 = Q(teacher__group=postgraduate.teacher.group, is_group=True, date=datetime.today())
                temp_setting = TempCheckInSetting.objects.filter(q1 | q2).all()
            else:
                temp_setting = TempCheckInSetting.objects.filter(teacher=postgraduate.teacher,
                                                                 date=datetime.today()).all()
            for setting in temp_setting:
                json['temp_id'].append(setting.id)
                json['temp_name'].append(setting.name)
                json['temp_time'].append(setting.time.strftime('%H:%M'))
                json['temp_time_interval'].append('{}-{}'.format(setting.start_time.strftime('%H:%M'),
                                                                 setting.end_time.strftime('%H:%M')))
            records_ok = TempCheckIn.objects.filter(target__in=temp_setting, postgraduate=postgraduate).all()
            for record in records_ok:
                json['temp_ok'].append(record.target.id)
        return JsonResponse(json)


@csrf_exempt
def check_in(request):
    """签到逻辑"""
    json = {
        'auth_result': False,
        'status_code': -1  # -1:条件不符合；0：长周期二维码（继续扫描）；1：签到成功；-2：时间不符合
    }
    if request.method == 'POST':
        token = request.POST.get('token')
        code = request.POST.get('code')
        type_ = int(request.POST.get('type'))
        index = int(request.POST.get('index'))
        postgraduate = verify_postgraduate_by_jwt(token)
        if postgraduate:
            json['auth_result'] = True
            if len(code) > 64:
                computer_index = int(code[64:])
                computer = Computer.objects.get(id=computer_index)
                check_in_code = CheckInCode(cpu_id=computer.cpu_id)
            else:
                check_in_code = CheckInCode()
            code_, is_valid = check_in_code.get_code()
            if code == code_:
                if is_valid:
                    # 扫描的是短期二维码，进行签到
                    if type_ == 1:
                        # 日常签到
                        setting = DailyCheckInSetting.objects.get(teacher=postgraduate.teacher)
                        # 检查设置的条件是否满足
                        if setting.computer.exists():
                            if not check_in_code.get_computer() in setting.computer.all():
                                # 签到设置中限定计算机，且计算机不符
                                return JsonResponse(json)
                        # 检查时间是否符合设置区间
                        start = 'time{}_start'.format(index)
                        end = 'time{}_end'.format(index)
                        if not getattr(setting, start) < datetime.now().time() < getattr(setting, end):
                            json['status_code'] = -2
                            return JsonResponse(json)
                        # 条件均符合，执行签到
                        record = DailyCheckIn.objects.filter(date=datetime.today(), postgraduate=postgraduate)
                        if record.exists():
                            record = record[0]
                        else:
                            record = DailyCheckIn.objects.create(date=datetime.today(), postgraduate=postgraduate)
                        setattr(record, 'check{}'.format(index), datetime.now().time())  # 将当前时间写入对应的属性
                        record.save()
                        json['status_code'] = 1
                    # 临时签到
                    if type_ == 2:
                        setting = TempCheckInSetting.objects.get(id=index)
                        # 检查设置的条件是否满足
                        if setting.computer.exists():
                            if not check_in_code.get_computer() in setting.computer.all():
                                # 签到设置中限定计算机，且计算机不符
                                return JsonResponse(json)
                        # 检查日期
                        if setting.date != datetime.today().date():
                            json['status_code'] = -2
                            return JsonResponse(json)
                        # 检查时间是否符合设置区间
                        if not setting.start_time < datetime.now().time() < setting.end_time:
                            json['status_code'] = -2
                            return JsonResponse(json)
                        # 条件均符合，执行签到
                        TempCheckIn.objects.create(target=setting, postgraduate=postgraduate,
                                                   date_time=datetime.now())
                        json['status_code'] = 1
                else:
                    # 扫描的是长期二维码，创建短期二维码
                    check_in_code.generate_code('s')
                    json['status_code'] = 0
        return JsonResponse(json)


def decrypt_data(data):
    """RSA解密数据"""
    f = open("master-private.pem", 'r')
    priv_key = RSA.importKey(f.read())
    cipher = PKCS1_OAEP.new(priv_key, hashAlgo=SHA256)
    data = base64.b64decode(data)
    return cipher.decrypt(data).decode("utf-8")
