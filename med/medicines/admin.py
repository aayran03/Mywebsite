# medicines/admin.py
from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse,path
from django.http import HttpResponseRedirect
from .models import Medicine
import pandas as pd
from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse
from django import forms



@admin.action(description='Sort by name')
def sort_by_name(modeladmin, request, queryset):
    return HttpResponseRedirect(reverse('admin:medicines_medicine_changelist') + '?o=1')

@admin.action(description='Sort by expiry date')
def sort_by_expiry_date(modeladmin, request, queryset):
    return HttpResponseRedirect(reverse('admin:medicines_medicine_changelist') + '?o=2')

@admin.action(description='Sort by quantity')
def sort_by_quantity(modeladmin, request, queryset):
    return HttpResponseRedirect(reverse('admin:medicines_medicine_changelist') + '?o=3')

@admin.action(description='Mark selected medicines as expired')
def mark_as_expired(modeladmin, request, queryset):
    queryset.update(expiry_date='2000-01-01')
    messages.success(request, 'Selected medicines have been marked as expired.')

@admin.action(description='Increase quantity by 10 for selected medicines')
def increase_quantity(modeladmin, request, queryset):
    for medicine in queryset:
        medicine.quantity += 10
        medicine.save()
    messages.success(request, 'Quantity increased by 10 for selected medicines.')

@admin.action(description='Delete selected medicines')
def delete_medicines(modeladmin, request, queryset):
    queryset.delete()
    messages.success(request, 'Selected medicines have been deleted.')



class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification_number', 'expiry_date', 'quantity')
    search_fields = ('name', 'identification_number')
    actions = [mark_as_expired, increase_quantity, delete_medicines]




admin.site.register(Medicine, MedicineAdmin)
