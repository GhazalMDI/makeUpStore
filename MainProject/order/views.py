from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from order.forms import ReceiverForm, CopounForm
from products.models import Product, Variant
from accounts.models import Address
from order.models import Coupon, Order, OrderItem
import jdatetime
from cart.cart import Cart, VariantCart
import random
from utils.pg import *

PG_URL = 'https://panel.aqayepardakht.ir/startpay/sandbox'

class ShoppingView(LoginRequiredMixin,View):
    template_name = 'order/order.html'
    form_class = ReceiverForm

    # form_Copoun = CopounForm

    def get(self, request):
        # form = self.form_Copoun(request.GET)
        # if form.is_valid():
        #     user_code = form.changed_data['code']
        #     now = jdatetime.datetime.now()
        #     if copoun := Coupon.objects.filter(code__exact=user_code, from_date__lte=now, to_date__gte=now,
        #                                        active=True).first():

        ctx = {
            # 'copoun': self.form_Copoun(),
            'cart': Cart(request),
            'Variant': VariantCart(request),
            'user_address': Address.objects.filter(user=request.user).first(),
            'form': self.form_class(instance=request.user)
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        address_get = Address.objects.filter(id=request.POST.get('address')).first()
        if form.is_valid():
            cd = form.cleaned_data
            request.session['receiver_information'] = {
                'address': address_get.id,
                'receiver_fname': cd.get('first_name'),
                'receiver_lname': cd.get('last_name'),
                'receiver_tel': cd.get('phone_number'),
            }
            ctx = {
                # 'copoun': self.form_Copoun(),
                'cart': Cart(request),
                'Variant': VariantCart(request),
                'user_address': Address.objects.filter(user=request.user).first(),
                'form': self.form_class(instance=request.user),
                'receiver': request.session.get('receiver_information'),
                'address_user': address_get

            }
            return render(request, self.template_name, ctx)
        ctx = {
            # 'copoun': self.form_Copoun(),
            'cart': Cart(request),
            'Variant': VariantCart(request),
            'user_address': Address.objects.filter(user=request.user).first(),
            'form': form,
            'receiver': request.session.get('receiver_information'),
            'address_user': address_get
        }
        return render(request, self.template_name, ctx)


class SendOrderView(LoginRequiredMixin,View):
    def post(self, request):
        if session_receiver := request.session.get('receiver_information'):
            address_user = Address.objects.filter(id=session_receiver['address'],user=request.user).first()

            order = Order.objects.create(
                user=request.user,
                phone_number=session_receiver['receiver_tel'],
                first_name=session_receiver['receiver_fname'],
                last_name=session_receiver['receiver_lname'],
                address=address_user
            )
            del session_receiver

        else:
            order = Order.objects.create(
                user=request.user,
                phone_number=request.user.phone_number,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                address=Address.objects.filter(user=request.user).first()
            )

        for i in Cart(request):
            obj = OrderItem.objects.create(
                product_id=i['id'],
                order=order,
                price=i['after_dis'] if 'after_dis' in i and i['after_dis'] > 0 else i['price'],
                quantity=i['quantity']
            )
            obj.save()

        for v in VariantCart(request):
            after_dis = v.get('after_dis')
            price = after_dis if after_dis is not None and after_dis > 0 else v['price']
            obj = OrderItem.objects.create(
                variant_id=v['id'],
                order=order,
                price=price,
                quantity=v['quantity']
            )
            obj.save()

        return redirect('order:OrderCreate', order.id)


class OrderCreateView(LoginRequiredMixin,View):
    template_name = 'order/createOrder.html'
    form_class = CopounForm

    def get(self, request, id):
        if user_order := get_object_or_404(Order, pk=id):
            user_order.buy = user_order.get_total_order
            user_order.save()
            ctx = {
                'form': self.form_class(),
                'order': user_order
            }
            return render(request, self.template_name, ctx)

        return redirect('cart:cartShow')

    def post(self, request, id):
        order = get_object_or_404(Order, pk=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code']
            now = jdatetime.datetime.now()
            if coupon := Coupon.objects.filter(code__exact=user_code, from_date__lte=now, to_date__gte=now,
                                               active=True).first():
                if coupon.more and coupon.less and coupon.less < order.get_total_order < coupon.more and not coupon.user.filter(
                        id=request.user.id).exists():
                    order.discount = coupon.discount
                    coupon.user.add(request.user)
                    order.save()
                    print('hi 4')

                elif coupon.less and order.get_total_order > coupon.less and not coupon.more and not coupon.user.filter(
                        id=request.user.id).exists():
                    order.discount = coupon.discount
                    coupon.user.add(request.user)
                    order.save()
                    print('hi 2')

                elif coupon.more and order.get_total_order < coupon.more and not coupon.less and not coupon.user.filter(
                        id=request.user.id).exists():
                    order.discount = coupon.discount
                    coupon.user.add(request.user)
                    order.save()
                    print('hi 3')

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        ctx = {
            'order': order,
            'form': form
        }
        return render(request, self.template_name, ctx)


class StartPayView(LoginRequiredMixin,View):
    def get(self, request, id):
        if order := get_object_or_404(Order, pk=id, paid=False):
            order.invoice_id = random.randint(100000000, 9000000000)
            order.save()
            data = {
                'invoice_id': order.invoice_id,
                'amount': order.get_total_order
            }
            response = create(data)
            res = response.json()
            if response.status_code == 200 and res.get('status') == 'success':
                return redirect(f'{PG_URL}/{res.get("transid")}')
            order.status = res.get('code')
            order.err = get_error(res.get('code'))
            order.save()
            return redirect('cart:cartShow')

        return redirect(request, '404.html')


class VerifyPayView(View):
    template_name = 'order/verifyOrder.html'

    def post(self, request):
        data = request.POST
        if order := get_object_or_404(Order, invoice_id=data.get('invoice_id')):
            login(request, order.user)
            order.cardnumber = data.get('cardnumber')
            order.bank = data.get('bank')
            order.tracking_number = data.get('tracking_number')
            order.transid = data.get('transid')
            order.status = data.get('status')
            order.save()

            if data.get('status') == '1':
                data = {
                    'amount': order.buy,
                    'transid': order.transid,
                }
                response = verify(data)
                res = response.json()
                if response.status_code == 200 and res.get('status') == 'success' and res.get('code') == '1':
                    order.paid = True
                    order.save()
                    item = order.order_order_items.all()

                    for i in item:
                        if i.product:
                            product = get_object_or_404(Product, pk=i.product.id)
                            product.stock -= i.quantity
                            product.sale += i.quantity
                            if product.stock == 0:
                                product.is_available = False
                            product.save()

                        if i.variant:
                            variant = get_object_or_404(Variant, pk=i.variant.id)
                            variant.stock -= i.quantity
                            variant.sale += i.quantity
                            if variant.stock == 0:
                                variant.is_available = False
                            variant.save()

                    ctx = {
                        'order': order
                    }
                    return render(request, self.template_name, ctx)
                order.status = res.get('code')
                order.err = get_error(res.get('code'))
                order.save()
                ctx = {
                    'order': order
                }
                return render(request, self.template_name, ctx)

            err = get_error(data.get('status'))
            order.status = data.get('status')
            order.err = err
            order.save()

            ctx = {
                'order': order
            }

            return render(request, self.template_name, ctx)

        return redirect('404.html')
