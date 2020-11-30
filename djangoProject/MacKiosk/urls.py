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
from django.urls import path
from .view import *

app_name = 'MacKiosk'

urlpatterns = [
    path('', index, name='index'),
    path('kiosk/menus', menuSelect, name='menuSelect'),
    path('kiosk/howmany', howmany, name='howmany'),
    path('kiosk/selectPay',selectPay, name='selectPay'),
    path('kiosk/basket',basket, name='basket'),
    path('kiosk/inputcash',inputcash,name='inputcash'),
    path('kiosk/inputcard',inputcash,name='inputcard'),
    path('kiosk/complete',complete,name='complete'),
    path('kiosk/reset/', reset, name='reset'),
    path('kiosk/<int:pk>/cancelMenu/', cancelMenu, name='cancelMenu'),
    ]
'''
    path('kiosk/basket', toCart, name='toCart'),
    path('kiosk/quantity/', quantitySelect, name='quantitySelect'),
    path('kiosk/addCart/', addCart, name='addCart'),

    path('kiosk/toCart/', toCart.as_view(), name='toCart'),
    path('kiosk/payment/', payment, name='payment'),
    path('kiosk/chQty/', chQty, name='chQty'),
    path('kiosk/complete/', complete, name='complete'),
    path('kiosk/showOrderNum/', showOrderNum, name='showOrderNum'),

    path('seller/postmenu/', postmenu, name='postmenu'),
    path('seller/callList/', callList.as_view(), name='callList'),
    path('sellet/orderList/', orderList.as_view(), name='orderList'),
    path('seller/callCustomer/', callCustomer, name='callCustomer'),
    path('seller/menuComplete/', menuComplete, name='menuComplete'),
    path('seller/cancelOrder/', cancelOrder, name='cancelOrder'),
    path('seller/orderIngrd/', orderIngrd, name='orderIngrd'),
    path('seller/srchIngrd/', srchIngrd.as_view(), name='srchIngrd'),
    path('seller/srchTerm/', srchTerm.as_view(), name='srchTerm'),
'''
