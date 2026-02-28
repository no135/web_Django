"""
URL configuration for parking project.

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
from parking_system.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    
    path('lot/add/', add_lot, name='add_lot'),
    path('lot/edit/<int:lot_id>/', edit_lot, name='edit_lot'),
    path('lot/delete/<int:lot_id>/', delete_lot, name='delete_lot'),
    path('lot/<int:lot_id>/', lot_detail, name='lot_detail'),
    path('lot/capacity/<int:lot_id>/', lot_capacity_check, name='lot_capacity_check'),
    
    path('spot/toggle/<int:spot_id>/', maintenance_toggle, name='maintenance_toggle'),
    path('spots/all/', spot_list_all, name='spot_list_all'),
    
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicle/edit/<int:vehicle_id>/', vehicle_edit, name='vehicle_edit'),
    path('vehicle/search/', vehicle_search, name='vehicle_search'),
    
    path('tickets/active/', active_tickets, name='active_tickets'),
    path('ticket/exit/<int:ticket_id>/', vehicle_exit, name='vehicle_exit'),
    path('ticket/delete/<int:ticket_id>/', ticket_delete, name='ticket_delete'),
    
    path('payments/', payment_history, name='payment_history'),
    path('payment/delete/<int:pay_id>/', delete_payment_record, name='delete_payment_record'),
    path('revenue/', revenue_stats, name='revenue_stats'),
    
    path('system/reset/', clear_all_history, name='clear_all_history'),
]
