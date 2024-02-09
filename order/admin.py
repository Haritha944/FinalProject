from django.contrib import admin
from order.models import Payment,Order,OrderItem,ReturnOrder,UserWallet
# Register your models here.
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ReturnOrder)
admin.site.register(UserWallet)