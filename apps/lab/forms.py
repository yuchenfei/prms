from django.forms import ModelForm

from lab.models import Experiment, Grade


class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = '__all__'


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
