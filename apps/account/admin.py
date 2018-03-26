import hashlib
from os import urandom

from django.contrib import admin

from .models import Teacher, Postgraduate, Group


def create_password(obj):
    # 创建盐
    obj.salt = urandom(32).hex()
    # 生成密码摘要
    obj.password = hashlib.pbkdf2_hmac('sha256', str.encode(obj.password), str.encode(obj.salt), 100000).hex()


class TeacherAdmin(admin.ModelAdmin):
    fields = ('username', 'password')

    def save_model(self, request, obj, form, change):
        create_password(obj)
        super().save_model(request, obj, form, change)


class PostgraduateAdmin(admin.ModelAdmin):
    exclude = ('uuid', 'salt')

    def save_model(self, request, obj, form, change):
        create_password(obj)
        super().save_model(request, obj, form, change)


class GroupAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        leader = obj.leader
        leader.group = obj
        leader.save()


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Postgraduate, PostgraduateAdmin)
admin.site.register(Group, GroupAdmin)
