from products.models import Product, Variant

CART_SESSION = 'cart'
VARIANT_CART_SESSION = 'variant_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get(CART_SESSION):
            self.session[CART_SESSION] = {}
        self.cart = self.session.get(CART_SESSION)

    def save(self):
        self.session.modified = True

    def addToCart(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'after_dis': product.after_discount}
        if self.cart[product_id]['quantity'] + quantity > product.stock:
            return False
        self.cart[product_id]['quantity'] += quantity
        self.save()
        return True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()
            return True
        else:
            return False

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for p in products:
            cart[str(p.id)]['image'] = p.image.url
            cart[str(p.id)]['name'] = p.name
            cart[str(p.id)]['discount'] = p.discount
            cart[str(p.id)]['after_dis'] = p.after_discount
            cart[str(p.id)]['profit'] = p.computing_profit
            cart[str(p.id)]['price'] = p.price
            cart[str(p.id)]['id'] = p.id
            cart[str(p.id)]['url'] = p.get_absolute_url
            cart[str(p.id)]['slug'] = p.slug
            # for v in p.extra_options.all():
            #     cart[str(p.id)]['value'] = v.value

        for item in cart.values():
            if item['after_dis']:
                item['total'] = item['quantity'] * item['after_dis']
            else:
                item['total'] = item['quantity'] * item['price']
            item['after_profit'] = item['quantity'] * item['profit']
            yield item

    @property
    def get_total_price(self):
        return sum(
            i['quantity'] * int(i['after_dis']) if i.get('after_dis') else i['quantity'] * int(i['price'])
            for i in self.cart.values())

    @property
    def get_total_profit(self):
        return sum(
            (int(i['price']) - int(i['profit'])) * int(i['quantity'])
            for i in self.cart.values()
            if 'profit' in i and i['profit'] and i['profit'] != 'False'
        )

    def __len__(self):
        return sum(
            1 for i in self.cart.values()
        )

    def clear_cart(self):
        del self.session[CART_SESSION]


class VariantCart:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get(VARIANT_CART_SESSION):
            self.session[VARIANT_CART_SESSION] = {}
        self.variant_cart = self.session.get(VARIANT_CART_SESSION)

    def save(self):
        self.session.modified = True

    def AddToVarinatCart(self, product, quantity):
        product_id = str(product.id)
        if not product_id in self.variant_cart:
            self.variant_cart[product_id] = {'quantity': 0, 'after_dis': product.after_discount}

        if self.variant_cart[product_id]['quantity'] + quantity > product.stock:
            return False

        self.variant_cart[product_id]['quantity'] += quantity
        self.save()
        return True

    def RemoveToCart(self, product):
        product_id = str(product.id)
        if product_id in self.variant_cart:
            if self.variant_cart[product_id]['quantity'] > 1:
                self.variant_cart[product_id]['quantity'] -= 1
            else:
                del self.variant_cart[product_id]
            self.save()
            return True
        else:
            return False

    def __iter__(self):
        product_ids = self.variant_cart.keys()
        variants = Variant.objects.filter(id__in=product_ids)
        variant = self.variant_cart.copy()

        for v in variants:
            variant[str(v.id)]['image'] = v.image.url
            variant[str(v.id)]['name'] = v.product.name
            variant[str(v.id)]['discount'] = v.discount
            variant[str(v.id)]['after_dis'] = v.after_discount
            variant[str(v.id)]['profit'] = v.computing_profit
            variant[str(v.id)]['price'] = v.price
            variant[str(v.id)]['id'] = v.id
            variant[str(v.id)]['url'] = v.product.get_absolute_url
            variant[str(v.id)]['slug'] = v.product.slug
            variant[str(v.id)]['color'] = v.color.name
            variant[str(v.id)]['number_color'] = v.color.number_color
            variant[str(v.id)]['color_code'] = v.color.color_code

        for item in variant.values():
            if item['after_dis']:
                item['total'] = item['quantity'] * item['after_dis']
            else:
                item['total'] = item['quantity'] * item['price']
            item['after_profit'] = item['quantity'] * item['profit']
            yield item

    @property
    def get_total_price(self):
        return sum(
            i['quantity'] * int(i['after_dis']) if i.get('after_dis') else i['quantity'] * int(i['price'])
            for i in self.variant_cart.values())

    @property
    def get_total_profit(self):
        return sum(
            (int(i['price']) - int(i['profit'])) * int(i['quantity'])
            for i in self.variant_cart.values()
            if 'profit' in i and i['profit'] and i['profit'] != 'False'
        )

    def __len__(self):
        return sum(
            1 for i in self.variant_cart.values()
        )
