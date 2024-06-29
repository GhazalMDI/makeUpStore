from django.db import models

from utils.baseModel import BaseModel
from django_jalali.db import models as jmodel


class Order(BaseModel):
    user = models.ForeignKey('accounts.User', models.CASCADE, 'order_user')
    address = models.TextField()
    phone_number = models.CharField(max_length=11, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    discount = models.PositiveIntegerField(default=0)
    buy = models.PositiveIntegerField(null=True)
    paid = models.BooleanField(default=False, null=True)
    invoice_id = models.CharField(max_length=255, null=True)
    err = models.CharField(null=True, max_length=255)
    status = models.CharField(null=True, max_length=255)
    cardnumber = models.CharField(max_length=16, null=True)
    tracking_number = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    transid = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.user.phone_number}-{self.user.last_name}'

    @property
    def get_total_order(self):
        total_price = sum(
            i.get_item_price for i in self.order_order_items.all()
        )
        if self.discount:
            return (100 - self.discount) * total_price // 100
        return total_price


class OrderItem(BaseModel):
    product = models.ForeignKey('products.Product', models.SET_NULL, 'product_order_items', null=True)
    variant = models.ForeignKey('products.Variant', models.SET_NULL, 'variant_order_items', null=True)
    order = models.ForeignKey('Order', models.SET_NULL, 'order_order_items', null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()





    @property
    def get_item_price(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    user = models.ManyToManyField('accounts.User', 'user_coupon', blank=True)
    active = models.BooleanField(default=True)
    discount = models.PositiveIntegerField(default=0)
    less = models.PositiveIntegerField(default=0, null=True, blank=True)
    more = models.PositiveIntegerField(default=0, null=True, blank=True)
    from_date = jmodel.jDateTimeField()
    to_date = jmodel.jDateTimeField()

    def __str__(self):
        return f'{self.code}'
