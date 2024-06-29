from django.urls import path
from home import views
app_name = 'Home'
urlpatterns = [
    path('',views.home.as_view(),name='home')

]