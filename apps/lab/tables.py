import django_tables2 as tabels

from .models import Experiment, Grade


class ExperimentTable(tabels.Table):
    class Meta:
        model = Experiment
        template_name = 'django_tables2/bootstrap.html'


class GradeTable(tabels.Table):
    class Meta:
        model = Grade
        template_name = 'django_tables2/bootstrap.html'
