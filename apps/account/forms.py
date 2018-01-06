from django import forms

from .models import Teacher, Postgraduate


class TeacherLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=False,
        error_messages={'required': '用户名不能为空'},
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入用户名',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=False,
        error_messages={'required': '密码不能为空'},
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入密码',
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data['username']
        is_username_exist = Teacher.objects.filter(username=username).exists()
        if not is_username_exist:
            raise forms.ValidationError('用户名不存在')

        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('密码至少为6位')

        return self.cleaned_data


class PostgraduateLoginForm(forms.Form):
    pid = forms.CharField(
        required=True,
        label=False,
        error_messages={'required': '学号不能为空'},
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入学号',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=False,
        error_messages={'required': '密码不能为空'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '输入密码',
            }
        ),
    )

    def clean(self):
        pid = self.cleaned_data["pid"]
        is_postgraduate_exist = Postgraduate.objects.filter(pid=pid).exists()
        if not is_postgraduate_exist:
            raise forms.ValidationError('学号不存在')

        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('密码至少为6位')

        return self.cleaned_data
