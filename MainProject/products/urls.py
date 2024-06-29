from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('',views.Products.as_view(),name='products'),
    path('<int:cat_id>/<cat_slug>/', views.Products.as_view(), name='products'),
    path('<int:cat_id>/', views.Products.as_view(), name='products_cat'),

    path('details/<int:id>/<slug>/',views.detailView.as_view(),name='details'),


    path('like/<int:productId>/',views.AddLikeView.as_view(),name='likeProduct'),
    path('varlike/<int:varproduct_id>/', views.AddLikeView.as_view(), name='likeVarProduct'),

    path('like/remove/<int:id>/', views.removeProductView.as_view(), name='removelikeProduct'),

]