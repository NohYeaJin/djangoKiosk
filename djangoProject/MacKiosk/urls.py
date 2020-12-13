"""MacKiosk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path

from . import view
from .view import *
from django.contrib import admin
from django.conf.urls import include, url
from ..djangoProject import settings

app_name = 'MacKiosk'

urlpatterns = [
    path('', index, name='index'),
    path('kiosk/menus', menuSelect, name='menuSelect'),
    path('kiosk/howmany/<int:menu_id>', howmany, name='howmany'),
    path('kiosk/selectPay',selectPay, name='selectPay'),
    path('kiosk/basket',basket, name='basket'),
    path('kiosk/inputcash',inputcash,name='inputcash'),
    path('kiosk/inputcard',inputcard,name='inputcard'),
    path('kiosk/complete',complete,name='complete'),
    path('kiosk/reset', reset, name='reset'),
    path('kiosk/reset2', reset2, name='reset2'),
    path('kiosk/addCart', addCart, name='addCart'),
    path('kiosk/cancelMenu/<int:cart_id>', cancelMenu, name='cancelMenu'),
    path('seller/orderList/', orderList.as_view(), name='orderList'),
    path('seller/<int:pk>/call/', call.as_view(), name='call'),
    path('seller/<int:pk>/orderComplete/',orderCompV.as_view(),name='order_complete'),
    path('seller/<int:pk>/orderCancel/',orderCancV.as_view(),name='order_cancel'),
    path('seller/callList/', callList.as_view(), name='callList'),
    path('seller/inventory/', inventory, name='inventory'),
    path('seller/inventory/<int:inven_id>', orderIngrd, name='orderIngrd'),
    path('seller/revenue/', revenue, name='revenue'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

