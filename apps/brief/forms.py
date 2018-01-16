from django.forms import ModelForm, Textarea

from .models import Brief


class BriefForm(ModelForm):
    class Meta:
        model = Brief
        fields = ('content', 'file')
        labels = {
            'content': '内容',
            'file': '文件'
        }
        widgets = {
            'content': Textarea(attrs={'class': 'form-control'})
        }


class InstructionsForm(ModelForm):
    class Meta:
        model = Brief
        fields = ('instructions',)
        labels = {
            'instructions': '批注'
        }
