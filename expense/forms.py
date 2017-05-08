from django import forms
from django.contrib.auth.models import User

from .models import Category, ExpenseItem, ReportItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_logo']


class ExpenseItemForm(forms.ModelForm):
    class Meta:
        model = ExpenseItem
        fields = ['item_category', 'item_name', 'item_cost', 'item_date']



class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportItem
        fields = ['start_date', 'end_date']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']