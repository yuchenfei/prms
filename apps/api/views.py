import base64
import jwt
import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.verification import verify_postgraduate_by_password
from api.models import Device


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
        print(json)
        return JsonResponse(json)


def decrypt_data(data):
    """RSA解密数据"""
    f = open("master-private.pem", 'r')
    priv_key = RSA.importKey(f.read())
    cipher = PKCS1_OAEP.new(priv_key, hashAlgo=SHA256)
    data = base64.b64decode(data)
    return cipher.decrypt(data).decode("utf-8")
