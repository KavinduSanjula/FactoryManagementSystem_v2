"""FactoryManagementSystem URL Configuration"""

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user_manager.urls')),
    path('inventory-manager/',include('inventory_manager.urls')),
    path('finance-manager/',include('finance_manager.urls')),
]
