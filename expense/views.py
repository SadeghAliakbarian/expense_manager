# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Category, ExpenseItem, ReportItem
from .forms import CategoryForm, ExpenseItemForm, ReportForm,UserForm
from django.contrib.auth import logout
from django.db.models import Sum

import numpy as np
import pandas as pd
# Create your views here.

def index(request):
    context = {}
    return render(request, 'expense/index.html', context)


def all_categories(request):
    if not request.user.is_authenticated():
        return render(request, 'expense/login.html')
    else:
        categories = Category.objects.all().filter(user = request.user)
        context = {'categories': categories}
        return render(request, 'expense/all_categories.html', context)


def all_expenses(request):
    if not request.user.is_authenticated():
        return render(request, 'expense/login.html')
    else:
        categories = ExpenseItem.objects.all().filter(item_category__user = request.user)
        context = {'items': categories}
        return render(request, 'expense/all_expenses.html', context)



IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
def create_category(request):
    if not request.user.is_authenticated():
        return render(request, 'expense/login.html')
    else:
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.category_name = request.POST['category_name']
                category.category_logo = request.FILES['category_logo']
                file_type = category.category_logo.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'category': category,
                        'form': form,
                        'error_message': 'Logo file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'expense/create_category.html', context)
                category.save()
                return render(request, 'expense/all_categories.html',{'categories': Category.objects.all()})

        context = {"form": form,}
        return render(request, 'expense/create_category.html', context)



def add_expense(request):
    if not request.user.is_authenticated():
        return render(request, 'expense/login.html')
    else:
        form = ExpenseItemForm(request.POST or None)
        if form.is_valid():
                item = form.save(commit=False)
                item.item_category = get_object_or_404(Category, pk = int(request.POST['item_category']))
                item.item_name = request.POST['item_name']
                item.item_cost = request.POST['item_cost']
                item.item_date = request.POST['item_date']

                item.save()
                return render(request, 'expense/all_expenses.html',{'items': ExpenseItem.objects.all()})

        context = {"form": form,}
        return render(request, 'expense/add_expense.html', context)



def report(request):
    if not request.user.is_authenticated():
        return render(request, 'expense/login.html')
    else:
        form  = ReportForm(request.POST or None)
        if form.is_valid():
            reporter = form.save(commit=False)
            reporter.start_date = request.POST['start_date']
            reporter.end_date = request.POST['end_date']

            expense_item_filtered = ExpenseItem.objects.all().filter(item_date__gte = reporter.start_date).filter(item_date__lte = reporter.end_date)
            expense_item_filtered = expense_item_filtered.filter(item_category__user = request.user)
            filtered_result = list(expense_item_filtered)

            # compute the sum of price
            total_price = expense_item_filtered.aggregate(Sum('item_cost'))

            context = {'data': filtered_result,
                       'form': form,
                       'date_from': reporter.start_date,
                       'date_to': reporter.end_date,
                       'total_price': (total_price)}
            return render(request, 'expense/report.html', context)
        return render(request, 'expense/report.html', {'form': form})




def item_category(request, category_id):
    pass


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'expense/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'expense/index.html', {})
            else:
                return render(request, 'expense/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'expense/login.html', {'error_message': 'Invalid login'})
    return render(request, 'expense/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'expense/index.html', {})
    context = {
        "form": form,
    }
    return render(request, 'expense/register.html', context)
