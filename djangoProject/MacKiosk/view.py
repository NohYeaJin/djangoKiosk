from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy

from mc.models import *

from datetime import datetime, timedelta
from random import *


def index(request, show='default'):
    return render(request, 'index2.html')


def menuSelect(request):
    return render(request, 'index.html')


def howmany(request):
    return render(request, 'howmany.html')

def selectPay(request):
    return render(request,'index3.html')


#메뉴선택화면으로
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

#장바구니로 가기
class toCart(ListView): #클래스형 뷰
    Model = Cart
    template_name = '장바구니.html'

#초기화 후 첫 화면
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

def complete(request):
    #Cart의 주문 정보를 Order로 옮김
    c_qs = Cart.objects.get()
    cus_num = randint(1, 1000)  #주문번호 랜덤생성
    o_qs = Orders(OrderNum=cus_num, OrderQty=c_qs.qty, OrderMenu=c_qs.name, OrderDate=datetime.today(), OrderPrice=c_qs.price)
    o_qs.save()
    return HttpResponseRedirect(reverse('MacKiosk:showOrderNum'))
    #문제점: 한 고객이 여러 메뉴를 동시에 주문하는 경우
    #최선책: 주문번호/날짜/주문금액 한개에 메뉴/수량 정보는 개수 제한 없이 입력 가능
    #차선책: 고객의 주문 메뉴 개수 대로 여러 개의 쿼리문 생성
    #주문완료, 주문취소에서도 동일 문제 발생

def showOrderNum(request, cus_num):
    o_qs = Orders.objects.get(OrderNum=cus_num)
    context = {'o_qs': o_qs}    #{{o_qs.OrderNum}} 형식으로 html에서 게시(확인필요)
    return render(request, 'complete.html', context)

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
