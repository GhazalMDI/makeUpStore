from django.shortcuts import render
from django.views import View
from collections import Counter

from home.models import Banner
from products.models import *


class home(View):
    template_name = 'home/home.html'

    def get(self, request):
        products = Product.objects.all()
        banners = Banner.objects.all()
        Best_selling_products = Product.objects.filter(sale__gte=30)[:10]
        Best_selling_variants = Variant.objects.filter(sale__gte=30)[:10]
        if request.user.is_authenticated:
            user_view = UserProductView.objects.filter(user=request.user).values('product_id')
            products_view = [v['product_id'] for v in user_view]
            similar_users = UserProductView.objects.filter(product_id__in=products_view).exclude(user=request.user)
            recommended_products = Counter([view.product_id for view in similar_users]).most_common(10)
            recommended_product_ids = [product_id for product_id, count in recommended_products]
            products = products.filter(id__in=recommended_product_ids)
            seen_products = SeenProduct.objects.filter(user=request.user)[:20]
            ctx = {
                'special_prodocts': Product.objects.filter(discount__gt=0),
                'banners': banners.filter(part='main'),
                'seconds_banners': banners.filter(part='second'),
                'Proposal': products,
                'seen_products': seen_products,
                'Best_selling_products': Best_selling_products,
                'Best_selling_variants': Best_selling_variants,
                'count_seen_products': seen_products.count()
            }
            return render(request, self.template_name, ctx)

        new_products = products.order_by('-created')[:10]

        ctx = {
            'special_prodocts': Product.objects.filter(discount__gt=0),
            'banners': banners.filter(part='main'),
            'seconds_banners': banners.filter(part='second'),
            'Best_selling_products': Best_selling_products,
            'Best_selling_variants': Best_selling_variants,
            'new_products':new_products,
        }
        return render(request, self.template_name, ctx)
