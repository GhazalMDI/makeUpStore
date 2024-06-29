from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product, SeenProduct, Variant
from cart.cart import Cart, VariantCart


class addToCartView(View,LoginRequiredMixin):
    # templates_name = 'accounts/Profile.html'
    def get(self, request, id, slug):
        product = get_object_or_404(Product, pk=id, slug=slug)
        if product:
            cart = Cart(request)
            if res := cart.addToCart(product, 1):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('products:products')


class removeProductToCartView(View,LoginRequiredMixin):
    def get(self, request, id, slug):
        if product := get_object_or_404(Product, id=id, slug=slug):
            cart = Cart(request)
            if res := cart.remove(product):
                return redirect('cart:cartShow')
            return redirect('products:products')


class cartView(View,LoginRequiredMixin):
    template_name = 'cart/cart.html'

    def get(self, request):
        seen_product = ''
        if request.user.is_authenticated:
            seen_product = SeenProduct.objects.filter(user=request.user).order_by('-created')
        ctx = {
            'cart': Cart(request),
            'variant': VariantCart(request),
            'cart_len': Cart(request).__len__(),
            'len_variant':VariantCart(request).__len__(),
            'seen_product': seen_product,
        }
        return render(request, self.template_name, ctx)


class clearView(View,LoginRequiredMixin):
    def get(self, request):
        del request.session['cart']
        del request.session['variant_cart']
        return redirect('cart:cartShow')


class addToVariantCartView(View,LoginRequiredMixin):
    def get(self, request, id):
        if product := get_object_or_404(Variant, pk=id):
            var_cart = VariantCart(request)
            if res := var_cart.AddToVarinatCart(product, 1):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('products:products')


class RemoveToVariantCartView(View,LoginRequiredMixin):
    def get(self, request, id):
        if product := get_object_or_404(Variant, pk=id):
            var_cart = VariantCart(request)
            if res := var_cart.RemoveToCart(product):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('products:products')
