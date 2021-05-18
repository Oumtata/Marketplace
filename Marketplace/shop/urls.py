from django.urls import path, include, re_path

import shop.views

urlpatterns = [
    path('', shop.views.show_items_not_owned, name = 'show_cart'),
    path('add', shop.views.add_to_cart, name = 'add_to_cart'),
    path('remove', shop.views.remove_from_cart, name = 'remove_item'),
    path('checkout', shop.views.checkout, name = 'checkout'),
    path('make_transaction', shop.views.make_transaction, name = 'make_transaction'),
    path('cart', shop.views.cart, name = 'cart'),
]