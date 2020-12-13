from django.contrib import admin
from .models import Order, Revenue
from .models import Menus
from .models import Inventory


class menuAdmin (admin.ModelAdmin):
    list_display = ('MenuName', 'MenuPrice')

class orderAdmin (admin.ModelAdmin):
    list_display = ('id', 'OrderNum', 'OrderQty', 'OrderMenu', 'OrderDate')

class inventoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'qty_base', 'price', 'origin',  'exprtdate_new')

class revenueAdmin(admin.ModelAdmin):
    list_display = ('id','order_num','content', 'sales', 'spend', 'salesdate')


admin.site.register(Order, orderAdmin)
admin.site.register(Menus, menuAdmin)
admin.site.register(Inventory, inventoryAdmin)
admin.site.register(Revenue, revenueAdmin)
