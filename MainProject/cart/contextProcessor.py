from cart.cart import Cart,VariantCart


def cartContext(request):
    return {
        'cart': Cart(request),
        'variant':VariantCart(request),
        'len_cart': Cart(request).__len__(),
        'len_variant':VariantCart(request).__len__(),
    }
