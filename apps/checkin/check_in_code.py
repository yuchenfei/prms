import hashlib
from os import urandom

from django.core.cache import cache

from .models import Computer


class CheckInCode(object):
    def __init__(self, cpu_id=None):
        self.cpu_id = cpu_id

    def get_computer(self):
        """获取对应的计算机信息对象，无则返回None"""
        if not self.cpu_id:
            return None

        if not Computer.objects.filter(cpu_id=self.cpu_id).exists():
            return None
        else:
            return Computer.objects.get(cpu_id=self.cpu_id)

    def __cache_name_l(self):
        prefix = 'qr_code_l'
        computer = self.get_computer()
        if computer:
            return prefix + '_' + str(computer.cpu_id)
        else:
            return prefix

    def __cache_name_s(self):
        prefix = 'qr_code_s'
        computer = self.get_computer()
        if computer:
            return prefix + '_' + str(computer.cpu_id)
        else:
            return prefix

    def generate_code(self, type):
        """生成二维码内容"""
        computer = self.get_computer()
        if computer:
            m = hashlib.md5()
            m.update(computer.cpu_id.encode('utf-8'))
            code = urandom(16).hex() + m.hexdigest() + str(computer.id)
        else:
            code = urandom(32).hex()

        if type == 'l':
            cache.set(self.__cache_name_l(), code, 15)
        elif type == 's':
            cache.set(self.__cache_name_s(), code, 5)
        return code

    def get_code(self):
        qr_code_s = cache.get(self.__cache_name_s(), None)
        if qr_code_s:
            return qr_code_s, True

        qr_code_l = cache.get(self.__cache_name_l(), None)
        if not qr_code_l:
            # 生成长时效二维码内容
            code = self.generate_code('l')
            return code, False
        else:
            return qr_code_l, False
