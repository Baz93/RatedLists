from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404

from .forms import VoteForm, RatersGroupForm, ItemForm, ListForm
from .models import List, Item, RatersGroup


def all_lists(request):
    paginator = Paginator(List.objects.all(), 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        displayed_lists = paginator.page(page)
    except PageNotAnInteger:
        displayed_lists = paginator.page(1)
    except EmptyPage:
        displayed_lists = paginator.page(paginator.num_pages)

    context = {
        'object_list': displayed_lists,
        'page_request_var': page_request_var,
        'user': request.user,
    }
    return render(request, 'all_lists.html', context)


def list_create(request):
    if not request.user.is_authenticated():
        raise Http404

    form = ListForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.save()

        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': 'New List',
        'button': 'Create',
        'delete': False,
    }
    return render(request, 'list_form.html', context)


def list_update(request, list_id):
    instance = get_object_or_404(List, id=list_id)

    if request.user != instance.owner:
        raise Http404

    form = ListForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.save()

        messages.success(request, 'Successfully Updated')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': instance.title,
        'instance': instance,
        'button': 'Update',
        'delete': True,
    }
    return render(request, 'list_form.html', context)


def list_delete(request, list_id=None):
    instance = get_object_or_404(List, id=list_id)

    if request.user != instance.owner:
        raise Http404

    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('index')


def list_view(request, list_id=None):
    instance = get_object_or_404(List, id=list_id)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    paginator = Paginator(instance.items.all(), 10)
    try:
        displayed_items = paginator.page(page)
    except PageNotAnInteger:
        displayed_items = paginator.page(1)
    except EmptyPage:
        displayed_items = paginator.page(paginator.num_pages)

    context = {
        'page_request_var': page_request_var,
        'object_list': displayed_items,
        'instance': instance,
        'user': request.user,
        'is_owner': request.user == instance.owner,
    }
    return render(request, 'list_view.html', context)


def list_chart(request, list_id=None):
    instance = get_object_or_404(List, id=list_id)

    form = RatersGroupForm(request.GET or None)
    members = []
    except_members = []
    if form.is_valid():
        if form.cleaned_data['all_except']:
            except_members = form.cleaned_data['members'].all()
        else:
            members = form.cleaned_data['members'].all()

    raters_group = RatersGroup.get_or_create(instance, members, except_members)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    paginator = Paginator(raters_group.scores.all(), 10)
    try:
        displayed_items = paginator.page(page)
    except PageNotAnInteger:
        displayed_items = paginator.page(1)
    except EmptyPage:
        displayed_items = paginator.page(paginator.num_pages)

    context = {
        'page_request_var': page_request_var,
        'object_list': displayed_items,
        'instance': instance,
        'form': form,
        'member_var': 'members',
        'user': request.user,
        'is_owner': request.user == instance.owner,
    }
    return render(request, 'list_chart.html', context)


def vote(request, list_id=None):
    if not request.user.is_authenticated():
        raise Http404

    form = VoteForm(list_id, request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.list = List.objects.get(id=list_id)
        instance.user = request.user
        instance.save()

        messages.success(request, 'Successfully Voted')
        return HttpResponseRedirect(instance.list.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'vote_form.html', context)


def item_detail(request, item_id=None):
    instance = get_object_or_404(Item, id=item_id)

    context = {
        'instance': instance,
        'is_owner': request.user == instance.list.owner,
    }
    return render(request, 'item_detail.html', context)


def item_create(request, list_id=None):
    list_instance = get_object_or_404(List, id=list_id)

    if request.user != list_instance.owner:
        raise Http404

    form = ItemForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.suggested_by = request.user
        instance.modified_by = request.user
        instance.list = list_instance
        instance.save()

        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': 'New Item',
        'button': 'Create',
        'delete': False,
    }
    return render(request, 'item_form.html', context)


def item_update(request, item_id=None):
    instance = get_object_or_404(Item, id=item_id)

    if request.user != instance.list.owner:
        raise Http404

    form = ItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.modified_by = request.user
        instance.save()

        messages.success(request, 'Successfully Updated')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': instance.title,
        'instance': instance,
        'button': 'Update',
        'delete': True,
    }
    return render(request, 'item_form.html', context)


def item_delete(request, item_id=None):
    instance = get_object_or_404(Item, id=item_id)
    instance_list = instance.list

    if request.user != instance_list.owner:
        raise Http404

    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect(instance_list.get_absolute_url())

