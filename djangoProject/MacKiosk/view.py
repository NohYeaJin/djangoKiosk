from django.shortcuts import render


def index(request, show='default'):
    return render(request, 'index2.html')


def menuSelect(request):
    return render(request, 'index.html')


#메뉴선택화면으로
def toMenu(request):
    return render(request, 'menu.html')

#장바구니 담기
def addCart(request):
    return redirect('menu.html')

#장바구니로 가기
def toCart(request):
    return render(request, 'cart.html')

#초기화 후 첫 화면
def reset(request):
    #장바구니 삭제
    return redirect('selplace.html')

#장바구니에서 수량 변경
def chQty(request):
    return redirect('장바구니.html')

#장바구니에서 메뉴 취소
def cancelMenu(request):
    #Cart DB에서 메뉴 삭제
    return redirect('장바구니.html')

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
    return render(request, 'complete.html')

#################################################
#판매자쪽 view

#메뉴 게시
def postmenu(request):
    #메뉴 DB에 메뉴 넣기
    return render(request, '판매자 메뉴 페이지')

#고객 호출
def callCustomer(request):
    return render(request, '주문관리 페이지')

#주문 과정 완료
def menuComplete(request):
    return render(request, '주문관리 페이지')

#주문 취소
def cancelOrder(request):
    return render(request, '주문관리 페이지')

#발주
def orderIngrd(request):
    return render(request, '재고관리 페이지')

#재료 조회
def srchIngrd(request):
    return render(request, '재고관리 페이지')

#매출 조회
def srchTerm(request):
    return render(request, '매출관리 페이지')

#판매자 메인 화면으로 가기
def returnMain(request):
    return render(request, '판매자 메인 페이지')