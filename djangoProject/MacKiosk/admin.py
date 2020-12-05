from django.contrib import admin
from .models import Orders, Cart
from .models import Menus
from .models import Inventory


class menuAdmin (admin.ModelAdmin):
    list_display = ('MenuName', 'MenuPrice')

class orderAdmin (admin.ModelAdmin):
    list_display = ('OrderNum', 'OrderQty', 'OrderMenu', 'OrderDate')

class inventoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'qty_base', 'price', 'origin', 'exprtdate')

class CartAdmin (admin.ModelAdmin):
    list_display = ('CartMenu', 'CartQty', 'CartPrice')

admin.site.register(Orders, orderAdmin)
admin.site.register(Menus, menuAdmin)
admin.site.register(Inventory, inventoryAdmin)
admin.site.register(Cart, CartAdmin)
