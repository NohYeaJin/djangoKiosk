import django

from django.db import models

#메뉴(판매자쪽 앱으로 보내는건 어떨까)
class Menus(models.Model):

    MenuName = models.CharField('MenuName', max_length=50, primary_key=True)
    MenuPrice = models.IntegerField('MenuPrice')
    #image = models.ImageField(upload_to='djangoProject/MacKiosk/static/images/')

    def __str__(self):
        return [self.MenuName, self.MenuPrice]

    class Meta:
        managed = False
        db_table = 'menus'

#장바구니
class Cart(models.Model):

    name = models.CharField('CartMenu', max_length=50, primary_key=True)
    qty = models.IntegerField('CartQty')
    price = models.IntegerField('CartPrice')

    def __str__(self):
        return self.name

    #class Meta:
     #   managed = False
      #  db_table = 'cart'

#주문현황(판매자쪽 앱)
class Orders(models.Model):

    OrderNum = models.IntegerField('OrderNum',primary_key=True)
    OrderQty = models.IntegerField('OrderQty')
    OrderMenu = models.CharField('OrderMenu', max_length=50)
    OrderDate = models.DateField('OrderDate')

    def __str__(self):
        return [self.OrderNum, self.OrderQty,self.OrderMenu,self.OrderDate]


    def get_order_num(self):
        return self.OrderNum

    def get_order_qty(self):
        return self.OrderQty

    def get_menu_name(self):
        return self.MenuName

    def get_order_date(self):
        return self.OrderDate

    class Meta:
     managed = False
     db_table = 'orders'

#재고(판매자쪽 앱)
class Inventory(models.Model):

    name = models.CharField('IngrdName', max_length=50, primary_key=True)
    qty = models.IntegerField('IngrdQty')
    price = models.IntegerField('IngrdPrice')
    origin = models.CharField('IngrdOrigin', max_length=50)
    exprtdate = models.DateTimeField('ExprtDate')

    def __str__(self):
        return [self.name,self.qty,self.price,self.origin,self.exprdate]

    class Meta:
     managed = False
     db_table = 'inventory'

#매출(판매자쪽 앱)
class Revenue(models.Model):

    sales = models.IntegerField('Sales')
    spend = models.IntegerField('Spend')
    netprofit = models.IntegerField('NetProfit')
    #saleshistory = models.
    salesdate = models.DateField('SalesDate', primary_key=True) #클래스 다이어그램에는 saleshistory로 쓰려고 했으나..
                                            #리스트로 구현이 어렵기에 그냥 date로 하는 것은 어떨지..

    def __str__(self):
        return self.salesdate

    #class Meta:
     #   managed = False
      #  db_table = 'revenue'

#고객 호출 번호
class CallCustomer(models.Model):

    orderNum = models.IntegerField('orderNum')

    def __str__(self):
        return self.orderNum


