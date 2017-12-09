from django import forms


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
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': '输入密码',
            }
        ),
    )


class PostgraduateLoginForm(forms.Form):
    id = forms.CharField(
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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '输入密码',
            }
        ),
    )
