"""
URL configuration for maintainance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from maintain.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', order, name='order'),
    path('order/<str:order_name>/', order_detail, name='order_detail'),
    path('add-order/', add_order, name='add_order'),
    path('edit-order/<str:order_name>/', edit_order, name='edit_order'),
    path('delete-order/<str:order_name>/', delete_order, name='delete_order'),

    path('categories/', category_list, name='category_list'),
    path('add-category/', add_category, name='add_category'),
    path('edit-category/<str:cat_name>/', edit_category, name='edit_category'),
    path('delete-category/<str:cat_name>/', delete_category, name='delete_category'),

    path('specialities/', speciality_list, name='speciality_list'),
    path('add-speciality/', add_speciality, name='add_speciality'),
    path('edit-speciality/<str:spec_name>/', edit_speciality, name='edit_speciality'),
    path('delete-speciality/<str:spec_name>/', delete_speciality, name='delete_speciality'),

    path('assets/', asset_list, name='asset_list'),
    path('add-asset/', add_asset, name='add_asset'),
    path('edit-asset/<str:asset_name>/', edit_asset, name='edit_asset'),
    path('delete-asset/<str:asset_name>/', delete_asset, name='delete_asset'),

    path('technicians/', technician_list, name='technician_list'),
    path('add-technician/', add_technician, name='add_technician'),
    path('edit-technician/<str:tech_name>/', edit_technician, name='edit_technician'),
    path('delete-technician/<str:tech_name>/', delete_technician, name='delete_technician'),
    path('clientn/',clientn,name ='clientn'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)