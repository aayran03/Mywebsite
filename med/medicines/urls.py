# medicines/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
    path('upload/', views.upload, name= 'upload'),
    # other URLs for editing and deleting can be added similarly
]