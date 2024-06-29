from django.db import models
from utils.baseModel import BaseModel
from django.urls import reverse

from taggit.managers import TaggableManager


class Product(BaseModel):
    STATUS = (
        ('Color', 'color'),
        ('None', 'none'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=255)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/%Y/%M/%d')
    brand = models.ForeignKey('Brand', models.PROTECT, 'brand_product', null=True)
    firstCategory = models.ForeignKey('FirstCategory', models.PROTECT, null=True)
    secondCategory = models.ForeignKey('SecondCategory', models.PROTECT, null=True)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    status = models.CharField(choices=STATUS, max_length=255, default='None')
    stock = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    tag = TaggableManager()
    sale = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return f'{self.name}-{self.id}'

    @property
    def after_discount(self):
        unit_price = self.price
        if self.discount:
            unit_price = (100 - self.discount) * unit_price // 100
            return unit_price
        return False

    @property
    def computing_profit(self):
        unit_price = self.price
        if self.discount:
            unit_price = (100 - self.discount) * unit_price // 100
            return unit_price
        return False

    @property
    def get_absolute_url(self):
        return reverse('products:details', args=(self.id, self.slug))


class Variant(models.Model):
    product = models.ForeignKey('Product', models.CASCADE, 'variant_product')
    stock = models.PositiveIntegerField()
    color = models.ForeignKey('Color', models.CASCADE, 'var_color')
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='variant_color_product/%Y/%m/%D', null=True)
    is_available = models.BooleanField(default=True)
    sale = models.PositiveIntegerField(null=True, default=0)

    @property
    def computing_profit(self):
        unit_price = self.price
        if self.discount:
            unit_price = (100 - self.discount) * unit_price // 100
            return unit_price
        return False

    def __str__(self):
        return f'{self.product.name}-{self.color.name}-{self.price}'

    @property
    def after_discount(self):
        if self.discount:
            return (100 - self.discount) * self.price // 100


class Extra_Option(BaseModel):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey('Product', models.CASCADE, 'extra_options', null=True)


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Color(BaseModel):
    name = models.CharField(max_length=255)
    color_code = models.CharField(max_length=255, null=True, blank=True)
    number_color = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}-{self.number_color}'


class FirstCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class SecondCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    firstCategory = models.ForeignKey('FirstCategory', models.CASCADE, 'sub_category')
    image = models.ImageField(upload_to='products/category/%Y/%M/%d', null=True)

    def __str__(self):
        return self.name


class ImageGallery(models.Model):
    image = models.ImageField(upload_to='products/%Y/%M/%d')
    product = models.ForeignKey('Product', models.CASCADE, 'product_images')


class Comment(BaseModel):
    user = models.ForeignKey('accounts.User', models.CASCADE, 'comments_user')
    product = models.ForeignKey('Product', models.CASCADE, 'comment_product', null=True)
    body = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.phone_number}-{self.product.name}'


class SeenProduct(BaseModel):
    user = models.ForeignKey('accounts.User', models.CASCADE, 'seen_product_user')
    product = models.ForeignKey('Product', models.CASCADE, 'seen_product_product')

    def __str__(self):
        return f'{self.user.phone_number}-{self.product.name}'


class UserProductView(BaseModel):
    product = models.ForeignKey('Product', models.PROTECT, 'view_product_product')
    user = models.ForeignKey('accounts.User', models.CASCADE, 'view_product_user')
    view_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}-{self.view_count}'


class LikeProduct(BaseModel):
    product = models.ForeignKey('Product', models.CASCADE, 'product_like', blank=True, null=True)
    variant = models.ForeignKey('Variant', models.CASCADE, 'variant_like', blank=True, null=True)
    user = models.ForeignKey('accounts.User', models.CASCADE, 'like_user')

    def __str__(self):
        if self.product:
            return f'{self.product.name}-{self.user.phone_number}'
        else:
            return f'{self.variant.product.name}-{self.user.phone_number}'
