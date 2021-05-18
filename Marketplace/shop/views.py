from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib.auth.models import User
from shop.models import OrderItem, Cart, Transaction
import datetime
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
@login_required
def show_items_not_owned(request):
    context = {'user_prod': Product.objects.filter(~Q(owner = request.user))}
    (cart, created) = Cart.objects.get_or_create(user = request.user, is_ordered = False)
    context['all_order_items'] = cart.items.all()
    context['total_price'] = cart.get_cart_price()
    return render(request, 'shop/show_items_not_owned.html', context)

@login_required
def add_to_cart(request):
    context = {'other_items': Product.objects.filter(~Q(owner = request.user))}
    (cart, created) = Cart.objects.get_or_create(user = request.user, is_ordered = False)
    context['cart'] = cart
    context['all_items'] = cart.items.all()
    if request.method == 'POST':
        try:
            #Get the product
            prod = Product.objects.get(id=request.POST['id'])
            #If the product is owned by the user
            if prod.owner == request.user:
                raise ObjectDoesNotExist
            if float(request.POST['quantity']) > prod.inventory_count:
                raise ValueError
            # i = OrderItem(item=prod, quantity=request.POST['quantity'])
            (i, boolean) = OrderItem.objects.get_or_create(user = request.user, item=prod)
            if (i.quantity + decimal.Decimal(request.POST['quantity'])) > prod.inventory_count:
                raise ValueError
            i.quantity += decimal.Decimal(request.POST['quantity'])
            i.save()
            context['orderItem'] = prod
        
            cart.items.add(i)
            cart.save()
            context['mess'] = "ADDED ORDER ITEM TO CART"
        except ObjectDoesNotExist:
            context['mess'] = "NO SUCH PRODUCT ID"
            return render(request, 'shop/add_to_cart.html', context)
        except ValueError:
            context['mess'] = "CANNOT EXCEED THE REMAINING AMOUNT IN STOCK"
            return render(request, 'shop/add_to_cart.html', context)
    return render(request, 'shop/add_to_cart.html', context)

@login_required
def remove_from_cart(request):
    context = {}
    try:
        cart = Cart.objects.get(user=request.user)
        all_items_in_cart= cart.get_cart_items()
        context['all_items_in_cart'] = all_items_in_cart
        if request.method == 'POST':
            order = cart.items.get(id=request.POST['order_ID'])
            cart.items.remove(order)

            orderItem = OrderItem.objects.get(user = request.user, id=request.POST['order_ID'])
            orderItem.delete()
            
            context['mess'] = 'REMOVE COMPLETE'

    except ObjectDoesNotExist:
        context['mess'] = 'ORDER ITEM ID NOT VALID'
        return render(request, 'shop/error.html', context)
    except MultipleObjectsReturned:
        context['mess'] = 'MultipleObjectsReturned'
        return render(request, 'shop/error.html', context)
    return render(request, 'shop/remove_from_cart.html', context)

@login_required
def checkout(request):
    context = {}
    (cart, created) = Cart.objects.get_or_create(user = request.user, is_ordered = False)
    #If the cart was never created or if the cart exists, but is empty
    if created or cart.items.count() == 0:
        context['mess'] = 'You did not add any items in your cart'
        return render(request, 'shop/error.html', context)
    context['bool'] = True
    return render(request, 'shop/checkout.html', context)

@login_required
def make_transaction(request):
    context = {}
    cart = Cart.objects.get(user = request.user, is_ordered = False)
    #Update inventory count of ordered items
    continue_trans = True
    for p in cart.get_cart_items():
        if (p.item.inventory_count - p.quantity) < 0:
            continue_trans = False
    
    if continue_trans:
        for p in cart.get_cart_items():
            p.item.inventory_count -= p.quantity
            p.item.save()
        
        #Create a Transaction database record
        t = Transaction(
            user = request.user,
            amount = cart.get_cart_price())
        t.save()
        t.items.set(cart.get_cart_items())
        t.save()

        #remove orderItem
        OrderItem.objects.filter(user = request.user).delete()

        #Empty Cart
        cart.delete()
        return HttpResponseRedirect(reverse('show_cart'))
    else:
        context['mess'] = 'PLEASE REDO YOUR CART WITH UPDATED PRODUCT QUANTITIES'
        cart.delete()
        return render(request, 'shop/error.html', context)

@login_required
def cart(request):
    context = {'user_prod': Product.objects.filter(~Q(owner = request.user))}
    (cart, created) = Cart.objects.get_or_create(user = request.user, is_ordered = False)
    context['all_order_items'] = cart.items.all()
    context['total_price'] = cart.get_cart_price()
    return render(request, 'shop/cart.html', context)
