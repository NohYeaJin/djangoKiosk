from django.contrib import admin
from .models import Order
from .models import Menu
from .models import Inventory


class menuAdmin (admin.ModelAdmin):
    list_display = ('MenuName', 'MenuPrice')

class orderAdmin (admin.ModelAdmin):
    list_display = ('id', 'OrderNum', 'OrderQty', 'OrderMenu', 'OrderDate')

class inventoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'qty_base', 'price', 'origin', 'exprtdate')

admin.site.register(Order, orderAdmin)
admin.site.register(Menu, menuAdmin)
admin.site.register(Inventory, inventoryAdmin)
