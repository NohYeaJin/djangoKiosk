from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.dateformat import DateFormat
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy
import pandas as pd
from .models import *
from django.utils.dateformat import DateFormat

from datetime import datetime, timedelta
from random import *



def index(request):
    return render(request, 'index2.html')


def menuSelect(request, show='default'):
    total_price = 0
    c_qs = Cart.objects.all()
    for i in c_qs:
        total_price += i.CartPrice
    single = Menus.objects.filter(category='single')
    set = Menus.objects.filter(category='set')
    side = Menus.objects.filter(category='side')
    drink = Menus.objects.filter(category='drink')
    dessert = Menus.objects.filter(category='dessert')
    context = {'singles': single, 'sets': set, 'sides': side, 'drinks': drink, 'desserts': dessert,'total_price': total_price}


    return render(request, 'index(example).html', context)


def howmany(request, menu_id):
    temp = Menus.objects.get(id=menu_id)
    context = {'menu': temp}
    return render(request, 'howmany(example).html', context)



def selectPay(request):
    return render(request,'index3.html')

def basket(request):
    total_price = 0
    c_qs = Cart.objects.all()
    for i in c_qs:
        total_price += i.CartPrice
    cart_list = Cart.objects.all()
    context = {'cart_list': cart_list, 'total_price':total_price}
    return render(request, 'basket.html', context)


def inputcash(request):
    return render(request,'inputcash.html')

def inputcard(request):
    return render(request,'inputcard.html')


class orderList(ListView):
    model = Order
    template_name='orderlist.html'

class orderCompV(DeleteView):
    model = Order
    success_url = reverse_lazy('MacKiosk:orderList')

    def get(self, request, *args, **kwargs):
        o_qs = Order.objects.get(id=self.kwargs.get('pk'))
        r_qs = Revenue(content=o_qs.OrderMenu, spend=0, sales=o_qs.OrderPrice, salesdate=o_qs.OrderDate)
        r_qs.save()
        return self.post(request, *args, **kwargs)

class orderCancV(DeleteView):
    model = Order
    success_url=reverse_lazy('MacKiosk:orderList')

    def get(self, request, *args, **kwargs):
       return self.post(request, *args, **kwargs)

class call(View):
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        if queryset.count() != 1:
            status = Order.objects.get(id=self.kwargs.get('pk'))
            status.OrderComplete = True
            status.save()

        return HttpResponseRedirect(reverse('MacKiosk:orderList'))

class callList(ListView):
    model = Order
   # queryset = Order.objects.filter(OrderComplete=True)
    template_name='call_list.html'

def showOrderNum(request, cus_num):
    o_qs = Order.objects.get(OrderNum=cus_num)
    context = {'o_qs': o_qs}
    return render(request, 'complete.html', context)

def complete(request):
    c_qs = Cart.objects.all()
    #Cart의 주문 정보를 Order로 옮김
    num = randint(100, 1000)
    for i in c_qs:

        o_qs = Order(OrderMenu=i.CartMenu, OrderQty=i.CartQty, OrderDate=datetime.today(),OrderNum=num,
                      OrderPrice=i.CartPrice)
        o_qs.save()
    c_qs.delete()
    #o_qs = Orders(OrderNum=cus_num, OrderQty=c_qs.CartQty, OrderMenu=c_qs.CartMenu, OrderDate=datetime.today(), OrderPrice=c_qs.CartPrice)
    context = {'o_qs': o_qs}  # {{o_qs.OrderNum}} 형식으로 html에서 게시(확인필요)
    return render(request, 'complete.html', context)



def reset(request):
    c_qs = Cart.objects.all()
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:basket'))

def reset2(request):
    c_qs = Cart.objects.all()
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:menuSelect'))
#장바구니에서 메뉴 취소
def cancelMenu(request, cart_id):
    #Cart DB에서 메뉴 삭제
    c_qs = Cart.objects.get(id=cart_id)
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:basket'))

#장바구니 담기
def addCart(request):    #선택한 메뉴 기준
    menu_id = request.POST.get('MenuID')

    m_qs = Menus.objects.get(id=menu_id)
    add_qty = request.POST.get('MenuQty')
    add_qty=int(add_qty)
    add_price = (m_qs.MenuPrice) * add_qty
    c_qs = Cart(CartMenu=m_qs.MenuName, CartQty=add_qty, CartPrice=add_price)
    c_qs.save()

    return HttpResponseRedirect(reverse('MacKiosk:menuSelect'))

def revenue(request):
    if request.method == 'GET':
        temp = Revenue.objects.all().order_by('-id', 'salesdate')

        sales = 0
        for i in temp:
            sales += i.sales
        spend = 0
        for i in temp:
            spend += i.spend
        profit = sales - spend

        context = {'revenues': temp, 'sales':sales, 'spend':spend, 'profit':profit}
        return render(request, 'revenue.html', context)
    elif request.method == 'POST':
        start = request.POST['start']
        end = request.POST['end']
        temp = Revenue.objects.filter(salesdate__in=pd.date_range(start, end)).order_by('-id', 'salesdate')

        sales = 0
        for i in temp:
            sales += i.sales
        spend = 0
        for i in temp:
            spend += i.spend
        profit = sales - spend

        context = {'revenues': temp, 'sales':sales, 'spend':spend, 'profit':profit}
        return render(request, 'revenue.html', context)


def inventory(request):
    temp = Inventory.objects.all()
    context = {'inventories': temp}
    return render(request, 'inventory.html', context)

def orderIngrd(request, inven_id):
    Ingrd = Inventory.objects.get(id=inven_id)
    temp = Ingrd.qty_base - Ingrd.qty_now
    base = Ingrd.qty_base

    Ingrd.qty_now = base
    Ingrd.save()

    if temp != 0:
        add_content = Ingrd.name
        add_spend = temp * Ingrd.price
        add_salesdate = DateFormat(datetime.now()).format('Y-m-d')

        add = Revenue(content=add_content, spend=add_spend, salesdate=add_salesdate)
        add.save()

    return redirect('MacKiosk:inventory')

class managerMenu(ListView):
    model = Menus
    template_name = 'manager_menu.html'

class MenuAdd(CreateView):
    model = Menus
    fields = ['MenuName', 'MenuPrice', 'image']
    template_name = 'manu_add.html'
    success_url = reverse_lazy('manager_menu.html')

def MenuDelete(request, Mname):
    m_qs = Menus.objects.get(ManuName=Mname)
    m_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:managerMenu'))

