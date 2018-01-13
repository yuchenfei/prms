from django.forms import ModelForm, Textarea, ValidationError

from .models import GroupFile


class GroupFileForm(ModelForm):
    class Meta:
        model = GroupFile
        fields = ('title', 'describe', 'file')
        labels = {
            'title': '标题',
            'describe': '描述',
            'file': '文件'
        }
        widgets = {
            'describe': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if GroupFile.objects.filter(title=title).exists():
            raise ValidationError('标题已存在')
        return title
