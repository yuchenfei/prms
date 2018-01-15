from django.forms import ModelForm

from .models import Brief


class BriefForm(ModelForm):
    class Meta:
        model = Brief
        fields = ('content', 'file')
        labels = {
            'content': '内容',
            'file': '文件'
        }


class InstructionsForm(ModelForm):
    class Meta:
        model = Brief
        fields = ('instructions',)
        labels = {
            'instructions': '批注'
        }
