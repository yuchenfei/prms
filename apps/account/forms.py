from django.forms import Form, ModelForm, \
    CharField, TextInput, PasswordInput, ModelMultipleChoiceField, \
    ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Teacher, Postgraduate, Group


class TeacherLoginForm(Form):
    phone = CharField(
        required=True,
        label=False,
        error_messages={'required': '手机号不能为空'},
        widget=TextInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入手机号',
            }
        ),
    )
    password = CharField(
        required=True,
        label=False,
        error_messages={'required': '密码不能为空'},
        widget=PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入密码',
            }
        ),
    )

    def clean(self):
        phone = self.cleaned_data['phone']
        is_phone_exist = Teacher.objects.filter(phone=phone).exists()
        if not is_phone_exist:
            raise ValidationError('手机号不存在')

        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError('密码至少为6位')

        return self.cleaned_data


class PostgraduateLoginForm(Form):
    phone = CharField(
        required=True,
        label=False,
        error_messages={'required': '手机号不能为空'},
        widget=TextInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入手机号',
            }
        ),
    )
    password = CharField(
        required=True,
        label=False,
        error_messages={'required': '密码不能为空'},
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '输入密码',
            }
        ),
    )

    def clean(self):
        phone = self.cleaned_data["phone"]
        is_postgraduate_exist = Postgraduate.objects.filter(phone=phone).exists()
        if not is_postgraduate_exist:
            raise ValidationError('手机号不存在')

        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError('密码至少为6位')

        return self.cleaned_data


class GroupTeacherMemberForm(Form):
    teacher_member = ModelMultipleChoiceField(
        queryset=Teacher.objects.filter(lead_group=None, group=None).all(),  # 过滤非组长、未加入组的教师
        required=False,
        widget=FilteredSelectMultiple("教师", is_stacked=False),
    )

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        exclude = ('uuid', 'password', 'salt', 'group')
        error_messages = {
            'phone': {
                'required': '手机号不能为空',
            },
            'name': {
                'required': '姓名不能为空',
            },
        }


class PostgraduateForm(ModelForm):
    class Meta:
        model = Postgraduate
        exclude = ('uuid', 'password', 'salt', 'teacher')
        error_messages = {
            'phone': {
                'required': '手机号不能为空',
            },
            'name': {
                'required': '姓名不能为空',
            },
        }
