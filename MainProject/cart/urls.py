from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('',views.cartView.as_view(),name='cartShow'),

    # product
    path('addToCart/<int:id>/<slug>/',views.addToCartView.as_view(),name='addCart'),
    path('removeProductToCart/<int:id>/<slug>/',views.removeProductToCartView.as_view(),name='removeProduct'),


    # variant urls
    path('addToVariantCart/<int:id>/',views.addToVariantCartView.as_view(),name='addVariantCart'),
    path('removeVariantProductToCart/<int:id>/', views.RemoveToVariantCartView.as_view(), name='removeVariantProduct'),

    path('clear/',views.clearView.as_view(),name='clear')


]