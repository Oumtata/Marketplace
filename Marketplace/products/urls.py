from django.urls import path, include, re_path

import products.views
import accounts.views
import shop.views
import chat.views




urlpatterns = [
    path('', products.views.list_products, name = 'pre_login_home'),
    path('homepage', products.views.homepage, name = 'homepage'),
    path('add', products.views.add_page, name = 'add_page'),
    path('delete', products.views.delete_product, name = 'delete_product'),
    path('update', products.views.update_product, name = 'update_product'),
    # path('redirect/', products.views.myacc, name = 'redirect to accounts/myacc'),
    # path('logout', products.views.logout, name = 'logout'),
    path('myproducts', products.views.my_products, name = 'my_products'),
    # path('signup', accounts.views.signup, name = 'signup'),
    # path('login', accounts.views.do_login, name = 'do_login'),
    # path('show_cart', shop.views.show_cart, name = 'show_cart'),
    # path('chat', chat.views.index, name='index'),
]