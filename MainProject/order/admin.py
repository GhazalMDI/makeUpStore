from django.contrib import admin
from order.models import *


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 2

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','address','first_name','last_name','discount')
    list_filter = ('user','address','discount')
    inlines = [OrderItemsInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','active','from_date','to_date','less','more')






