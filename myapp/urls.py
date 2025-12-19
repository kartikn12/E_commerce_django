from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('sindex/', views.sindex, name='sindex'), # seller index

    path('cart/', views.cart, name='cart'),
    path('detail/', views.detail, name='detail'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('fpass/', views.fpass, name='fpass'),
    path('otp/', views.otp, name='otp'),
    path('newpass/', views.newpass, name='newpass'),

    path('cpass/', views.cpass, name='cpass'),
    path('scpass/', views.cpass, name='scpass'), # seller

    path('uprofile/', views.uprofile, name='uprofile'),
    path('suprofile/', views.uprofile, name='suprofile'), # seller

    # seller
    path('add/', views.add, name='add'),
    path('view/', views.view, name='view'),
    path('pdetails/<int:pk>/', views.pdetails, name='pdetails'),

    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),

    path('addwish/<int:pk>/', views.addwish, name='addwish'),
    path('wish/', views.wish, name='wish'),
    path('bpdetails/<int:pk>/', views.bpdetails, name='bpdetails'),
    path('deletewish/<int:pk>/', views.deletewish, name='deletewish'),

    path('addcart/<int:pk>/', views.addcart, name='addcart'),
    path('cart/', views.cart, name='cart'),
    path('deletecart/<int:pk>/', views.deletecart, name='deletecart'),
    path('success/', views.success, name='success'),
    path('myorder/', views.myorder, name='myorder'),


]
