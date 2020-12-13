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


#메인 화면 렌더링
def index(request):
    return render(request, 'index2.html')

#매인 화면 카테고리별로 분류
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

#수량 선택 페이지
def howmany(request, menu_id):
    temp = Menus.objects.get(id=menu_id)
    context = {'menu': temp}
    return render(request, 'howmany(example).html', context)


#결제 수단을 묻는 페이지
def selectPay(request):
    return render(request,'index3.html')

#장바구니 페이지
def basket(request):
    total_price = 0
    c_qs = Cart.objects.all()
    for i in c_qs:
        total_price += i.CartPrice
    cart_list = Cart.objects.all()
    context = {'cart_list': cart_list, 'total_price':total_price}
    return render(request, 'basket.html', context)

#현금을 넣어달라는 화면
def inputcash(request):
    return render(request,'inputcash.html')

#카드를 삽입해달라는 화면
def inputcard(request):
    return render(request,'inputcard.html')

#판매자 view의 들어온 주문 목록들이 출력되는 페이지
class orderList(ListView):
    model = Order
    template_name='orderlist.html'

#메뉴 판매 완료 후 주문이 매출에 수입으로 들어가는 과정 
class orderCompV(DeleteView):
    model = Order
    success_url = reverse_lazy('MacKiosk:orderList')

    def get(self, request, *args, **kwargs):
        o_qs = Order.objects.get(id=self.kwargs.get('pk'))
        r_qs = Revenue(order_num = o_qs.OrderNum ,content=o_qs.OrderMenu, spend=0, sales=o_qs.OrderPrice, salesdate=o_qs.OrderDate)
        r_qs.save()
        return self.post(request, *args, **kwargs)

#판매자가 주문 취소
class orderCancV(DeleteView):
    model = Order
    success_url=reverse_lazy('MacKiosk:orderList')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#판매자가 조리 완료 후 고객 호출
class call(View):
    def get(self, request, *args, **kwargs):
        status = Order.objects.get(id=self.kwargs.get('pk'))
        status.OrderComplete = True
        status.save()

        return HttpResponseRedirect(reverse('MacKiosk:orderList'))

#고객 호출 리스트
class callList(ListView):
    model = Order
   # queryset = Order.objects.filter(OrderComplete=True)
    template_name='call_list.html'

#주문번호 출력
def showOrderNum(request, cus_num):
    o_qs = Order.objects.get(OrderNum=cus_num)
    context = {'o_qs': o_qs}
    return render(request, 'complete.html', context)

#Cart의 주문 정보를 Order로 옮김
def complete(request):
    c_qs = Cart.objects.all()
    num = randint(100, 1000)
    for i in c_qs:
        o_qs = Order(OrderMenu=i.CartMenu, OrderQty=i.CartQty, OrderDate=datetime.today(),OrderNum=num,
                      OrderPrice=i.CartPrice)
        o_qs.save()
    c_qs.delete()
    context = {'o_qs': o_qs}  # {{o_qs.OrderNum}} 형식으로 html에서 게시
    return render(request, 'complete.html', context)


#장바구니 초기화(장바구니 화면에서)
def reset(request):
    c_qs = Cart.objects.all()
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:basket'))

#장바구니 초기화(메인 메뉴에서)
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

#수익 계산
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

#재고 관리
def inventory(request):
    temp = Inventory.objects.all()
    context = {'inventories': temp}
    return render(request, 'inventory.html', context)

#재고 발주
def orderIngrd(request, inven_id):
    Ingrd = Inventory.objects.get(id=inven_id)
    base = Ingrd.qty_base

    d = timedelta(Ingrd.term)
    Ingrd.exprtdate_new = d + datetime.now()
    Ingrd.save()

    add_content = Ingrd.name
    add_spend = Ingrd.qty_base * Ingrd.price
    add_salesdate = DateFormat(datetime.now()).format('Y-m-d')

    add = Revenue(order_num=0, content=add_content, spend=add_spend, salesdate=add_salesdate)
    add.save()

    return redirect('MacKiosk:inventory')



