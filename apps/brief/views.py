from datetime import datetime

import os

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from account.models import Postgraduate, Teacher
from account.views import get_login_user, login_required
from .forms import BriefForm, InstructionsForm
from .models import Brief


@login_required
def brief_list(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')
        user = get_login_user(request)
        if user.__class__ in [Teacher, Postgraduate]:
            if isinstance(user, Postgraduate):
                postgraduate = user
                response = dict(postgraduate=postgraduate)
                template_name = 'brief/brief_list_p.html'
                briefs = Brief.objects.filter(submitter=postgraduate)
            else:
                teacher = user
                response = dict(teacher=teacher)
                template_name = 'brief/brief_list_t.html'
                postgraduates = Postgraduate.objects.filter(teacher=teacher)
                briefs = Brief.objects.filter(submitter__in=postgraduates, commit=True)
            briefs = briefs.order_by('-date')
            paginator = Paginator(briefs, 5)
            try:
                _list = paginator.page(int(page))
            except PageNotAnInteger:
                _list = paginator.page(1)
                page = 1
            except EmptyPage:
                _list = paginator.page(paginator.num_pages)
                page = paginator.num_pages
            response['brief_list'] = _list
            response['range'] = paginator.page_range
            response['page'] = int(page)
            return render(request, template_name, response)


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
                return redirect('brief_list_t')
        else:
            form = InstructionsForm(instance=brief)
        response_data['form'] = form
    else:
        response_data['postgraduate'] = user
    return render(request, 'brief/html_review.html', response_data)


@login_required
def delete(request, brief_id):
    if request.method == 'GET':
        brief = Brief.objects.get(id=brief_id)
        if brief:
            brief.delete()
            messages.add_message(request, messages.SUCCESS, '成功删除')
        return redirect('brief_list_p')
