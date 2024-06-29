from django.urls import path

from order import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'order'

urlpatterns = [
    path('order/', views.ShoppingView.as_view(), name='Shopping'),
    path('SendOrder/', views.SendOrderView.as_view(), name='SendOrder'),
    path('OrderCreate/<int:id>/', views.OrderCreateView.as_view(), name='OrderCreate'),

    path('startPay/<int:id>/', views.StartPayView.as_view(), name='startPay'),
    path('verifyPay/', csrf_exempt(views.VerifyPayView.as_view()), name='verifyPay'),

]
