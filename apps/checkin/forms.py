from django.forms import ModelForm, TextInput, ValidationError, HiddenInput

from .models import Computer


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
