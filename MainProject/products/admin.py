from django.contrib import admin
from products.models import *


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 1


class ExteraOptionInline(admin.TabularInline):
    model = Extra_Option
    extra = 2


class VariantInline(admin.TabularInline):
    model = Variant
    readonly_fields = ('sale',)
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'discount', 'sale')
    list_filter = ('name', 'created', 'price', 'is_available')
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = [ImageGalleryInline, ExteraOptionInline, VariantInline]
    readonly_fields = ('sale',)


@admin.register(FirstCategory)
class FirstCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(SecondCategory)
class FirstCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(LikeProduct)
class LikeProductAdmin(admin.ModelAdmin):
    list_display = ('product','variant', 'user')


@admin.register(Brand)
class FirstCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'number_color')


@admin.register(UserProductView)
class UserProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'view_count')
    list_filter = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body','user','accepted')



admin.site.register(SeenProduct)
