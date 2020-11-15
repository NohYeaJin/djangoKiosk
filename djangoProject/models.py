import django

from django.db import models


class Menus(models.Model):

    MenuName = models.CharField('MenuName')
    MenuPrice = models.IntegerField('MenuPrice')

    def __str__(self):
        return self.MenuName

    class Meta:
        managed = False
        db_table = 'menus'



class Orders(models.Model):

    OrderNum = models.IntegerField('OrderNum')
    OrderQty = models.IntegerField('OrderQty')
    MenuName = models.CharField('OrderMenu', max_length=50)
    OrderDate = models.DateField('OrderDate')

    def get_order_num(self):
        return self.OrderNum

    def get_order_qty(self):
        return self.OrderQty

    def get_menu_name(self):
        return self.MenuName

    def get_order_date(self):
        return self.OrderDate




