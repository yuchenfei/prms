from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from account.views import get_login_user
from .forms import ExperimentForm, GradeForm
from .tables import ExperimentTable, GradeTable
from .models import Experiment, Grade


def ex_list(request):
    response = dict()
    response['teacher'] = teacher = get_login_user(request)
    table = ExperimentTable(Experiment.objects.all())
    RequestConfig(request).configure(table)
    response['table'] = table
    return render(request, 'lab/ex_list.html', response)


def ex_add(request):
    response = dict()
    response['teacher'] = teacher = get_login_user(request)
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ex_list')
    else:
        form = ExperimentForm()
    response['form'] = form
    return render(request, 'lab/ex_add.html', response)


def grade_list(request):
    response = dict()
    response['teacher'] = teacher = get_login_user(request)
    table = GradeTable(Grade.objects.all())
    RequestConfig(request).configure(table)
    response['table'] = table
    return render(request, 'lab/ex_list.html', response)


def grade_add(request):
    response = dict()
    response['teacher'] = teacher = get_login_user(request)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    response['form'] = form
    return render(request, 'lab/grade_add.html', response)
