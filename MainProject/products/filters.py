import django_filters
from django import forms

from products.models import Brand, Product


class ProductsFilter(django_filters.FilterSet):
    sort_price = (
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
        ('جدیدترین', 'جدیدترین'),
        ('پرتخفیف ها', 'پرتخفیف ها')
    )
    price1 = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price2 = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # available = django_filters.BooleanFilter(field_name='is_available', widget=forms.CheckboxInput,
    #                                          method='filter_available', initial=False)
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    sort = django_filters.ChoiceFilter(choices=sort_price, method='get_sort_price',
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    # def filter_available(self, queryset, value, name):
    #     if value:
    #         return queryset.filter(is_available=True)
    #     return queryset

    def get_sort_price(self, queryset,name, value ):

        if value == 'ارزان ترین':
            o = 'price'
            # return queryset.order_by(o)
        if value == 'گران ترین':
            o = '-price'
            # return queryset.order_by(o)
        if value == 'پرتخفیف ها':
            o = '-discount'
            # return queryset.order_by(o)
        if value == 'جدیدترین ها':
            o = '-created'

        return queryset.order_by(o)
