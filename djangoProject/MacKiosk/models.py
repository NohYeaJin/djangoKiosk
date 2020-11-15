import django

from django.db import models


class Menus(models.Model):

    MenuName = models.CharField('MenuName',max_length=50,primary_key=True)
    MenuPrice = models.IntegerField('MenuPrice')

    def __str__(self):
        return [self.MenuName, self.MenuPrice]

    class Meta:
        managed = False
        db_table = 'menus'

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




