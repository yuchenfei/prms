import base64

import jwt
import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.verification import verify_postgraduate_by_password, verify_postgraduate_by_jwt
from checkin.models import Computer, DailyCheckIn, CheckInSetting, MeetingCheckIn
from checkin.check_in_code import CheckInCode
from .models import Device


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        json = {'result': False,
                'token': '',
                'reason': 0}
        pid = request.POST.get('pid')
        password = request.POST.get('password')
        imei = request.POST.get('imei')

        # 解密数据
        pid = decrypt_data(pid)
        password = decrypt_data(password)
        imei = decrypt_data(imei)

        postgraduate = verify_postgraduate_by_password(pid, password)
        if postgraduate:
            if not Device.objects.filter(postgraduate=postgraduate).exists():
                Device.objects.create(postgraduate=postgraduate, imei=imei)
            else:
                if not postgraduate.device.imei:
                    postgraduate.device.imei = imei
                elif postgraduate.device.imei != imei:
                    json['reason'] = 1
                    return JsonResponse(json)
            payload = {
                'iat': int(time.time()),  # 签发时间
                'exp': int(time.time()) + 86400 * 7,  # 过期时间
                'sub': str(postgraduate.pid),
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
    json = {
        'auth_result': False,
        'index': 0,
        'meeting_index': [],
        'meeting_time': [],
        'meeting_ok': []
    }
    if request.method == 'POST':
        token = request.POST.get('token')
        postgraduate = verify_postgraduate_by_jwt(token)
        if postgraduate:
            json['auth_result'] = True
            daily_check_in = DailyCheckIn.objects.filter(date=datetime.now().date(), postgraduate=postgraduate)
            if daily_check_in.exists():
                if daily_check_in[0].forenoon_in:
                    json['index'] = 1
                if daily_check_in[0].forenoon_out:
                    json['index'] = 2
                if daily_check_in[0].afternoon_in:
                    json['index'] = 3
                if daily_check_in[0].afternoon_out:
                    json['index'] = 4
            today = datetime.today()
            records = CheckInSetting.objects.filter(teacher=postgraduate.teacher, date_time__date=today, c_type=2,
                                                    enable=True).all()
            for record in records:
                json['meeting_index'].append(record.id)
                json['meeting_time'].append(record.date_time.time().strftime('%H:%M'))

            records_ok = MeetingCheckIn.objects.filter(target__in=records, postgraduate=postgraduate).all()
            for record in records_ok:
                json['meeting_ok'].append(record.target.id)
            print(json)

    return JsonResponse(json)


@csrf_exempt
def check_in(request):
    json = {
        'auth_result': False,
        'status_code': -1
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
                        today = datetime.now().date()
                        current_time = datetime.now().time()
                        record = DailyCheckIn.objects.filter(date=today, postgraduate=postgraduate)
                        if record.exists():
                            record = record[0]
                        else:
                            record = DailyCheckIn.objects.create(date=today, postgraduate=postgraduate)
                        if index == 1:
                            print('1 ok')
                            record.forenoon_in = current_time
                        elif index == 2:
                            record.forenoon_out = current_time
                        elif index == 3:
                            record.afternoon_in = current_time
                        elif index == 4:
                            record.afternoon_out = current_time
                        record.save()
                        json['status_code'] = 1
                    if type_ == 2:
                        setting = CheckInSetting.objects.get(id=index)
                        if setting.computer:
                            if not setting.computer == check_in_code.get_computer():
                                # 签到设置中限定计算机，且计算机不符
                                return JsonResponse(json)
                        MeetingCheckIn.objects.create(target=setting, postgraduate=postgraduate,
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
