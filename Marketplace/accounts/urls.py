from django.urls import path

import accounts.views
import products.views
import shop.views
import chat.views

urlpatterns = [
    path('', accounts.views.myacc, name = 'myacc'),
    path('signup', accounts.views.signup, name = 'signup'),
    path('login', accounts.views.do_login, name = 'acc_login'),
    path('logout', accounts.views.do_logout, name = 'do_logout'),
    path('myacc', accounts.views.myacc, name = 'myacc'),
    path('orderhist', accounts.views.orderhist, name = 'orderhist'),
    path('add', products.views.homepage, name = 'add_product'),
 ]
 