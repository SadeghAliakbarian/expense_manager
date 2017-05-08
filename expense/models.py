# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User

from django.db import models



class Category(models.Model):
    user = models.ForeignKey(User, default=1)
    category_name = models.CharField(max_length=100)
    category_logo = models.FileField()

    def __str__(self):
        return str(self.category_name)


class ExpenseItem(models.Model):
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_cost = models.FloatField(default=0.0)
    item_date = models.DateField()

    def __str__(self):
        return str(self.item_name)



class ReportItem(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()