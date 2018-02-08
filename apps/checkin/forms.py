from django.forms import ModelForm, TextInput, ValidationError, HiddenInput, DateTimeInput

from .models import Computer, CheckInSetting


class ComputerForm(ModelForm):
    class Meta:
        model = Computer
        fields = ('name', 'cpu_id')
        labels = {
            'title': '名称',
            'cpu_id': 'CPU '
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'cpu_id': HiddenInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cpu_id = self.cleaned_data['cpu_id']
        if Computer.objects.filter(cpu_id=cpu_id).exists():
            raise ValidationError('此计算机已录入')
        return self.cleaned_data


class CheckInSettingForm(ModelForm):
    class Meta:
        model = CheckInSetting
        fields = ('date_time', 'computer', 'enable')
        labels = {
            'date_time': '时间',
            'computer': '指定计算机',
            'enable': '使能'
        }
        widgets = {
            'date_time': DateTimeInput(format='%Y-%m-%d %H:%M')
        }
