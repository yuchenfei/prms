from django.forms import ModelForm, TextInput, ValidationError, HiddenInput, DateInput, CheckboxSelectMultiple

from .models import Computer, TempCheckInSetting, DailyCheckInSetting


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


class TempCheckInSettingForm(ModelForm):
    class Meta:
        model = TempCheckInSetting
        exclude = ['teacher']
        labels = {
            'name': '名称',
            'date': '日期',
            'time': '通知时间',
            'start_time': '签到开始时间',
            'end_time': '签到截至时间',
            'computer': '指定计算机',
        }
        widgets = {
            'date': DateInput(format='%Y-%m-%d'),
            'computer': CheckboxSelectMultiple()
        }


class DailyCheckInSettingForm(ModelForm):
    class Meta:
        model = DailyCheckInSetting
        exclude = ['teacher']
        labels = {
            'start_date': '开始日期',
            'end_date': '结束日期',
            'times': '每日签到次数',
            'time1_start': '开始时间',
            'time1_end': '结束时间',
            'computer': '指定计算机'
        }
        widgets = {
            'computer': CheckboxSelectMultiple(),
        }
