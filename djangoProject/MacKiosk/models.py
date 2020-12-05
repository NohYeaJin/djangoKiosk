import django

from django.db import models

#메뉴(판매자쪽 앱으로 보내는건 어떨까)
class Menu(models.Model):

    MenuName = models.CharField('MenuName', max_length=50, primary_key=True)
    MenuPrice = models.IntegerField('MenuPrice')
    #image = models.ImageField(upload_to='djangoProject/MacKiosk/static/images/')
    image = models.ImageField(upload_to='MacKiosk/static/images/', default=None)
    CATEGORIES = {
        ('single', 'Single'),
        ('set', 'Set Menu'),
        ('side', 'Side Menu'),
        ('drink', 'Drink'),
        ('dessert', 'Dessert')
    }
    category = models.CharField('Category', max_length=30, default='single', choices=CATEGORIES)

    def __str__(self):
        return self.MenuName

    class Meta:
        managed = False
        db_table = 'menus'

#장바구니
class Cart(models.Model):

    CartMenu = models.CharField('CartMenu', max_length=50,primary_key=True)
    CartQty = models.IntegerField('CartQty')
    CartPrice = models.IntegerField('CartPrice')

    def __str__(self):
        return self.name

    class Meta:
      managed = False
      db_table = 'cart'

#주문현황(판매자쪽 앱)
class Order(models.Model):

    id = models.AutoField(primary_key=True)
    OrderNum = models.IntegerField('OrderNum')
    OrderQty = models.IntegerField('OrderQty')
    OrderMenu = models.CharField('OrderMenu', max_length=50)
    OrderDate = models.DateField('OrderDate')
    OrderPrice = models.IntegerField('OrderPrice')
    OrderComplete=models.BooleanField('CompleteStatus',default=False)

    def __str__(self):
        return self.OrderMenu


    def get_order_num(self):
        return self.OrderNum

    def get_order_qty(self):
        return self.OrderQty

    def get_order_menu(self):
        return self.OrderMenu

    def get_order_date(self):
        return self.OrderDate

    class Meta:
     managed = False
     db_table = 'orders'

#재고(판매자쪽 앱)
class Inventory(models.Model):

    name = models.CharField('IngrdName', max_length=50)
    qty_base = models.IntegerField('IngrdQtybase')
    qty_now = models.IntegerField('IngrdQtynow')
    price = models.IntegerField('IngrdPrice')
    origin = models.CharField('IngrdOrigin', max_length=50)
    exprtdate = models.DateTimeField('ExprtDate')

    def __str__(self):
        return self.name

    class Meta:
     managed = False
     db_table = 'inventory'

#매출(판매자쪽 앱)
class Revenue(models.Model):

    id = models.AutoField(primary_key=True)
    content = models.CharField('Content', max_length=50)
    sales = models.IntegerField('Sales', blank=True, default=0)
    spend = models.IntegerField('Spend', blank=True, default=0)
    #netprofit = models.IntegerField('NetProfit')
    #saleshistory = models.
    salesdate = models.DateField('SalesDate', default=0000 - 00 - 00) #클래스 다이어그램에는 saleshistory로 쓰려고 했으나..
                                            #리스트로 구현이 어렵기에 그냥 date로 하는 것은 어떨지..

    def __str__(self):
        return str(self.salesdate)

    class Meta:
     managed = False
     db_table = 'revenue'

#고객 호출 번호
class CallCustomer(models.Model):

    orderNum = models.IntegerField('orderNum')

    def __str__(self):
        return str(self.orderNum)