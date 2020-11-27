from django.contrib import admin
from .models import Orders
from .models import Menus
from .models import Inventory


admin.site.register(Orders)
admin.site.register(Menus)
admin.site.register(Inventory)