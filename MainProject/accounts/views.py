from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from accounts.forms import RegisterForm, RegisterVerifyForm, EditAddressForm, UserInformation
from accounts.models import Otp, User, Address
from order.models import Order
from products.models import SeenProduct, LikeProduct, Comment
from random import randint
from cart.cart import Cart
from utils import sms, mapAPI
import jdatetime


# Create your views here.
class RegisterView(View):
    template_name = 'accounts/Register.html'
    form_class = RegisterForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        ctx = {
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            otp_instance, created = Otp.objects.get_or_create(phone_number=phone)
            if created:
                Random_code = randint(100000, 999999)
                otp_instance.code = Random_code
                otp_instance.save()
                request.session['user_phone'] = {
                    'phone_number': phone,
                    'next': self.next
                }
                sms.send_code(phone, Random_code)
                messages.add_message(request, 200, f'{Random_code}کد ورود شما', 'success')
                return redirect('accounts:RegisterVerify')
            otp_instance.delete()
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class RegisterVerifyView(View):
    template_name = 'accounts/RegisterVerify.html'
    form_class = RegisterVerifyForm

    def get(self, request):
        ctx = {
            'phone_number': request.session.get('user_phone')['phone_number'],
            'form': self.form_class
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        user_phone = request.session.get('user_phone')
        login_info = request.session.get('login_info')
        otp_instance = Otp.objects.filter(phone_number=user_phone.get('phone_number')).first()
        if form.is_valid():
            user_code = form.cleaned_data['code']
            if user_code == otp_instance.code:
                now = jdatetime.datetime.now()
                expire_time = otp_instance.created + jdatetime.timedelta(minutes=2)
                if now > expire_time:
                    otp_instance.delete()
                    del request.session['user_phone']
                    return redirect('accounts:Register')
                else:
                    user = User.object.filter(phone_number=user_phone.get('phone_number')).first()
                    if user:
                        login(request, user)
                        otp_instance.delete()

                        # if next_param := login_info.get('next'):
                        #     del request.session['login_info']
                        #     otp_instance.delete()
                        #     return redirect(next_param)
                    else:
                        user = User.object.create_user(phone_number=user_phone.get('phone_number'))
                        login(request, user)
                        if next_param := login_info.get('next'):
                            del request.session['login_info']
                            otp_instance.delete()
                            return redirect(next_param)
                        otp_instance.delete()
                        return redirect('Home:home')
            return redirect('Home:home')
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


class LogOutView(View):
    template_name = 'home/home.html'

    def get(self, request):
        logout(request)
        return redirect('Home:home')


class ProfileView(View):
    template_name = 'accounts/Profile.html'
    address_form = EditAddressForm
    profile_form = UserInformation

    def get(self, request):
        seen_products = SeenProduct.objects.filter(user=request.user)
        paginator = Paginator(seen_products, 10)
        page = request.GET.get('page')
        seen_products = paginator.get_page(page)
        url_data = request.GET.copy()
        if 'page' in url_data:
            del url_data['page']

        ctx = {
            'history_seens': seen_products,
            'comments': Comment.objects.filter(user=request.user),
            'address': Address.objects.filter(user=request.user),
            'form': self.profile_form(instance=request.user),
            'likes': LikeProduct.objects.filter(user=request.user),
            # 'seen_products': seen_products,
            'order_histories': Order.objects.filter(user=request.user, paid=True).order_by('-created')
        }

        return render(request, self.template_name, ctx)

    def post(self, request):
        seen_products = SeenProduct.objects.filter(user=request.user)

        paginator = Paginator(seen_products, 10)
        page = request.GET.get('page')
        seen_products = paginator.get_page(page)
        url_data = request.GET.copy()
        if 'page' in url_data:
            del url_data['page']
        form = self.profile_form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ctx = {
                'history_seens': seen_products,
                'comments': Comment.objects.filter(user=request.user),
                'address': Address.objects.filter(user=request.user),
                'form': self.profile_form(instance=request.user),
                'likes': LikeProduct.objects.filter(user=request.user),
                'order_histories': Order.objects.filter(user=request.user, paid=True)
            }
            return render(request, self.template_name, ctx)
        ctx = {
            'history_seens': seen_products,
            'comments': Comment.objects.filter(user=request.user),
            'address': Address.objects.filter(user=request.user),
            'pro_form': self.profile_form(instance=request.user),
            'likes': LikeProduct.objects.filter(user=request.user),
            'order_histories': Order.objects.filter(user=request.user, paid=True),
            'form': form
        }
        return render(request, self.template_name, ctx)


class AddressView(View):
    template_name = 'accounts/address.html'
    address_form = EditAddressForm

    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        if lat and lng:
            location = mapAPI.map(float(lat), float(lng))
            if location:
                request.session['address'] = {
                    'formatted_address': location.get('formatted_address'),
                    'state': location.get('state'),
                    'neighbourhood': location.get('neighbourhood')
                }
                print(request.session['address'])

        session_address = request.session.get('address', {})

        ctx = {
            'address': Address.objects.filter(user=request.user),
            'address_form': self.address_form(),
            'neighbourhood': session_address.get('neighbourhood', ''),
            'state': session_address.get('state', ''),
            'formatted_address': session_address.get('formatted_address', ''),
        }

        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.address_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not Address.objects.filter(user=request.user,
                                          formatted_address__exact=cd.get('formatted_address'),
                                          postal_code__exact=cd.get('postal_code')):
                ad = form.save(commit=False)
                ad.user = request.user
                ad.save()
                del request.session['address']
                return redirect('accounts:Profile')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            del request.session['address']

        ctx = {
            'address_form': form
        }
        return render(request, self.template_name, ctx)


class removeAddress(View):
    template_name = 'accounts/profile.html'

    def get(self, request, id_address):
        if address := get_object_or_404(Address, pk=id_address):
            address.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('404.html')
