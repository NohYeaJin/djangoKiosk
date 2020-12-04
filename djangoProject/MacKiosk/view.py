from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .models import *

from datetime import datetime, timedelta
from random import *

'''
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .cartforms import AddProductForm
from .cart import ClCart
'''


def index(request):
    return render(request, 'index2.html')


def menuSelect(request, show='default'):
    c_qs = Cart.objects.all()
    c_qs.delete()

    single = Menus.objects.filter(category='single')
    set = Menus.objects.filter(category='set')
    side = Menus.objects.filter(category='side')
    drink = Menus.objects.filter(category='drink')
    dessert = Menus.objects.filter(category='dessert')
    context = {'singles': single, 'sets': set, 'sides': side, 'drinks': drink, 'desserts': dessert}

    return render(request, 'index(example).html', context)


def howmany(request, menu_id):
    temp = Menus.objects.get(id=menu_id)
    context = {'menu': temp}
    return render(request, 'howmany.html', context)



def selectPay(request):
    return render(request,'index3.html')

def basket(request):
    c_qs = Cart.objects.all()
    context = {'cart_list': c_qs}
    return render(request, 'basket.html', context)

def inputcash(request):
    return render(request,'inputcash.html')

def inputcard(request):
    return render(request,'inputcard.html')


class orderList(TemplateView):
    template_name='seller_order.html'

class callList(TemplateView):
    template_name='call_list.html'


def showOrderNum(request, cus_num):
    o_qs = Orders.objects.get(OrderNum=cus_num)
    context = {'o_qs': o_qs}    #{{o_qs.OrderNum}} 형식으로 html에서 게시(확인필요)
    return render(request, 'complete.html', context)

def complete(request):
    #Cart의 주문 정보를 Order로 옮김
    c_qs = Cart.objects.all()
    num = Orders.objects.last().OrderNum
    num = num + 100
    for i in c_qs:

        o_qs = Orders(OrderMenu=i.CartMenu, OrderQty=i.CartQty, OrderDate=datetime.today(),OrderNum=num,
                      OrderPrice=i.CartPrice)
        o_qs.save()

    #o_qs = Orders(OrderNum=cus_num, OrderQty=c_qs.CartQty, OrderMenu=c_qs.CartMenu, OrderDate=datetime.today(), OrderPrice=c_qs.CartPrice)
    o_qs = Orders.objects.last()
    context = {'o_qs': o_qs}  # {{o_qs.OrderNum}} 형식으로 html에서 게시(확인필요)
    return render(request, 'complete.html', context)
    #문제점: 한 고객이 여러 메뉴를 동시에 주문하는 경우
    #최선책: 주문번호/날짜/주문금액 한개에 메뉴/수량 정보는 개수 제한 없이 입력 가능
    #차선책: 고객의 주문 메뉴 개수 대로 여러 개의 쿼리문 생성
    #주문완료, 주문취소에서도 동일 문제 발생
    
#초기화 후 첫 화면
def reset(request):
    #장바구니 삭제
    c_qs = Cart.objects.all()
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:menuSelect'))

#장바구니에서 메뉴 취소
def cancelMenu(request, Mname):
    #Cart DB에서 메뉴 삭제
    c_qs = Cart.objects.get(name=Mname)
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:basket'))

def revenue(request):
    if request.method == 'GET':
        temp = Revenue.objects.all()

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
        temp = Revenue.objects.filter(salesdate__in=pd.date_range(start, end))

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

'''
@require_POST

# 장바구니에 추가
def add(request, product_id):
    cart = ClCart(request)
    product = get_object_or_404(Menus, id=product_id)
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')

# 장바구니에서 삭제(삭제 예정)
def remove(request, product_id):
    cart = ClCart(request)
    product = get_object_or_404(Menus, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

# 장바구니 템플렛 페이지(basket.html) 위한 함수
def detail(request):
    cart = ClCart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update': True})
    return render(request, 'basket.html', {'cart': cart})
'''


'''
#메뉴선택화면으로


def howmany(request,menu_id):
   
    temp = Menus.objects.get(id=menu_id)
    context = {'menu': temp}
    return render(request, 'howmany.html', context)
    
    
def toMenu(request):
    return render(request, 'menu.html')

#장바구니 담기
def addCart(request, Mname):    #선택한 메뉴 이름 기준
    m_qs = Menus.objects.get(MenuName=Mname)

    add_name = Mname
    add_qty = request.POST['qty']   #버튼액션으로 수량 변경 방법을 모르겠습니다ㅠ 알게 되면 바로 수정하겠습니다. 혹시 아시는 분 수정헤 주시면 감사하겠습니다!
    add_price = m_qs.MenuPrice * add_qty

    c_qs = Cart(name=add_name, qty=add_qty, price=add_price)
    c_qs.save()

    return HttpResponseRedirect(reverse('MacKiosk:menuSelect'))




def reset(request):
    #장바구니 삭제
    c_qs = Cart.objects.all()
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:menuSelect'))

#장바구니에서 수량 변경
def chQty(request, Mname):
    #기존 저장된 메뉴 정보를 삭제하고 수량선택 화면으로 redirect해 다시 DB에 저장
    c_qs = Cart.objects.get(name=Mname)
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:quantitySelect'))

#장바구니에서 메뉴 취소
def cancelMenu(request, Mname):
    #Cart DB에서 메뉴 삭제
    c_qs = Cart.objects.get(name=Mname)
    c_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:toCart'))

#장바구니에서 메뉴 더 추가
def addMore(request):
    return redirect('menu.html')

#식사 장소 선택
def selPlace(request):
    return render(request, 'selplace.html')

def payment(request):
    return render(request, 'payment.html')

#결제 수단 선택
def pay(request, arg):
    if (arg==0):
        #arg를 DB에 보내고
        return render(request, 'cardpay.html')
    else:
        #arg를 DB에 보내고
        return render(request, 'cashpay.html')


#################################################
#판매자쪽 view

#메뉴 게시
class postmenu(CreateView):
    #메뉴 DB에 메뉴 넣기
    model = Menus
    fields = ['MenuName', 'MenuPrice', 'MenuPhoto']
    template_name = '메뉴추가_페이지.html'
    success_url = reverse_lazy('메뉴 저장 후 이동 html')

class callList(ListView):
    model = callCustomer
    template_name = '고객번호_호출.html'

class orderList(ListView):
    model = Orders
    template_name = '주문관리.html'

#고객 호출
def callCustomer(request, cusNum):
    o_qs = Orders.objects.get(OrderNum=cusNum)
    call_qs = CallCustomer(OrderNum=o_qs.OrderNum)
    call_qs.save()
    return HttpResponseRedirect(reverse('MacKiosk:주문관리'))

#주문 과정 완료
def menuComplete(request, cusNum):
    o_qs = Orders.objects.get(OrderNum=cusNum)
    i_qs = Inventory.objects.get(OrderMenu=o_qs.OrderMenu)

    i_qs.qty -= 1
    i_qs.save()
    r_qs = Revenue(sales=o_qs.MenuName, spend=0, netprofit=o_qs.OrderPrice, salesdate=o_qs.OrderDate)
    r_qs.save()
    return HttpResponseRedirect(reverse('MacKiosk:주문관리'))

#주문 취소
def cancelOrder(request, cusNum):
    o_qs = Orders.objects.get(OrderNum=cusNum)
    o_qs.delete()
    return HttpResponseRedirect(reverse('MacKiosk:주문관리'))

#발주
def orderIngrd(request, invenName):
    i_qs = Inventory.objects.get(name=invenName)

    i_qs.qty += 10  #한번에 재고 10개씩 주문(가정)
    i_qs.origin = datetime.today()
    i_qs.exprtdate = datetime.today() + timedelta(days=30)  #유효기간을 발주일로부터 30일 후로 설정(가정)
    i_qs.save()

    r_qs = Revenue(sales=i_qs.name, spend=(i_qs.price)*10, netprofit=0, salesdate=i_qs.origin)
    r_qs.save()
    return HttpResponseRedirect(reverse('MacKiosk:재고관리'))

#재료 조회
class srchIngrd(ListView):
    model = Inventory
    template_name = '재고관리.html'

#매출 조회
class srchTerm(ListView):
    model = Revenue
    template_name = '매출관리.html'

#판매자 메인 화면으로 가기
def returnMain(request):
    return render(request, '판매자 메인 페이지')
'''
