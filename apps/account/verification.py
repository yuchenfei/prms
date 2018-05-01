import hashlib

import jwt

from django.core.exceptions import ObjectDoesNotExist

from account.models import Teacher, Postgraduate


def verify_teacher_by_password(phone, password):
    teacher = Teacher.objects.get(phone=phone)
    password = hashlib.pbkdf2_hmac('sha256', str.encode(password), str.encode(teacher.salt), 100000).hex()
    if password == teacher.password:
        return teacher
    else:
        return None


def verify_postgraduate_by_password(phone, password):
    postgraduate = Postgraduate.objects.get(phone=phone)
    password = hashlib.pbkdf2_hmac('sha256', str.encode(password), str.encode(postgraduate.salt), 100000).hex()
    if password == postgraduate.password:
        return postgraduate
    else:
        return None


def verify_postgraduate_by_jwt(token):
    try:
        decoded = jwt.decode(token, 'secret', algorithm='HS256')
        # token有效，检索用户信息
        user = Postgraduate.objects.get(phone=decoded['sub'])
        return user
    except jwt.DecodeError:
        # token无法解析
        return None
    except jwt.ExpiredSignatureError:
        # token无效会捕获此异常
        return None
    except ObjectDoesNotExist:
        # 对象不存在
        return None
