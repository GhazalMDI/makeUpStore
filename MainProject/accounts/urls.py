from django.urls import path
from accounts import views
app_name = 'accounts'

urlpatterns = [
    path('Register/',views.RegisterView.as_view(),name='Register'),
    path('RegisterVerify/', views.RegisterVerifyView.as_view(), name='RegisterVerify'),
    path('Logout/', views.LogOutView.as_view(), name='Logout'),

    path('Profile/',views.ProfileView.as_view(),name='Profile'),

    path('address/',views.AddressView.as_view(),name='address'),
    path('address/delete/<int:id_address>/',views.removeAddress.as_view(),name='removeAddress'),

]