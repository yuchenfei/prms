from datetime import datetime

import os
from django.shortcuts import render, redirect

from account.models import Postgraduate, Teacher
from account.views import get_login_user, login_required
from .forms import BriefForm, InstructionsForm
from .models import Brief


@login_required
def brief_list_p(request):
    response_data = dict()
    response_data['postgraduate'] = postgraduate = get_login_user(request)
    response_data['brief_list'] = Brief.objects.filter(submitter=postgraduate).all()
    return render(request, 'brief/brief_list_p.html', response_data)


@login_required
def brief_list_t(request):
    response_data = dict()
    response_data['teacher'] = teacher = get_login_user(request)
    postgraduates = Postgraduate.objects.filter(teacher=teacher).all()
    response_data['brief_list'] = Brief.objects.filter(submitter__in=postgraduates).all()
    return render(request, 'brief/brief_list_t.html', response_data)


@login_required
def new(request):
    response_data = dict()
    response_data['postgraduate'] = postgraduate = get_login_user(request)
    if request.method == 'POST':
        form = BriefForm(request.POST, request.FILES)
        if form.is_valid():
            brief = form.save(commit=False)
            brief.submitter = postgraduate
            brief.date = datetime.now().date()
            if request.POST.get('save'):
                pass
            elif request.POST.get('commit'):
                brief.commit = True
            brief.save()
            return redirect('brief_list_p')
    else:
        form = BriefForm()
    response_data['form'] = form
    return render(request, 'brief/brief_new.html', response_data)


@login_required
def edit(request, brief_id):
    response_data = dict()
    response_data['postgraduate'] = postgraduate = get_login_user(request)
    brief = Brief.objects.get(id=brief_id)
    old_file = brief.file
    if request.method == 'POST':
        form = BriefForm(request.POST, request.FILES, instance=brief)
        if form.is_valid():
            brief = form.save(commit=False)
            if brief.file != old_file:
                try:
                    os.remove(old_file.path)
                except:
                    pass
            brief.date = datetime.now().date()
            if request.POST.get('save'):
                pass
            elif request.POST.get('commit'):
                brief.commit = True
            brief.save()
            return redirect('brief_list_p')
    else:
        form = BriefForm(instance=brief)
    response_data['form'] = form
    return render(request, 'brief/brief_new.html', response_data)


@login_required
def review(request, brief_id):
    response_data = dict()
    user = get_login_user(request)
    response_data['brief'] = brief = Brief.objects.get(id=brief_id)
    if isinstance(user, Teacher):
        response_data['teacher'] = user
        if not brief.have_read:
            brief.have_read = True
            brief.save()
        if request.method == 'POST':
            form = InstructionsForm(request.POST, instance=brief)
            if form.is_valid():
                form.save()
        else:
            form = InstructionsForm(instance=brief)
        response_data['form'] = form
    else:
        response_data['postgraduate'] = user
    return render(request, 'brief/html_review.html', response_data)
