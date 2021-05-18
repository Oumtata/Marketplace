from django.shortcuts import render
# from products.models import *
from .models import Product
# from . import forms
from .forms import ProductForm
from .models import get_upload_path
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def list_products(request):
    products = Product.objects.all()
    context = {'all_products': products}
    return render(request, 'products/list_products.html', context)

@login_required
def homepage(request):
    # simply list all the products that exist
    context = {'all_products': Product.objects.all()}
    return render(request, 'products/homepage.html', context)

@login_required
def delete_product(request):
    context = {'user_prod': Product.objects.filter(owner = request.user)}
    if request.method == 'POST':
        try:
            if request.POST['id'] == '':
                context['mess'] = "please insert an ID"
                return render(request, 'products/delete_product.html', context)
            prod = Product.objects.get(id = request.POST['id'])
            if request.user == prod.owner:
                context['mess'] = "Product deleted!"
                prod.delete()
            else:
                context['mess'] = "Cannot delete a product from another user"
        except ObjectDoesNotExist:
            context['mess'] = "Product id non-existant"
            return render(request, 'products/delete_product.html', context)
    return render(request, 'products/delete_product.html', context)
    
@login_required
def update_product(request):
    context = {'user_prod': Product.objects.filter(owner = request.user)}
    if request.method == 'POST':
        try:
            prod = Product.objects.get(id = request.POST['id'])
            if request.user == prod.owner:
                if request.POST['name'] != '':
                    prod.name = request.POST['name']
                if request.POST['description'] != '':
                    prod.description = request.POST['description']
                if request.POST['price'] != '':
                    prod.price = request.POST['price']
                if request.POST['inventory_count'] != '':
                    prod.inventory_count = request.POST['inventory_count']
                # if request.POST['image'] != '':
                #     prod.image = get_upload_path(prod, request.POST['image'])
                context['mess'] = "Update complete!"
                prod.save()
            else:
                context['mess'] = "Cannot update a product from another user"
        except ObjectDoesNotExist:
            context['mess'] = "Product id non-existant"
            return render(request, 'products/update_product.html', context)
    return render(request, 'products/update_product.html', context)


@login_required
#List the products of the current user
def my_products(request):
    context = {'user_prod': Product.objects.filter(owner = request.user)}
    return render(request, 'products/my_products.html', context)

@login_required
def add_page(request):
    #function to add a product to the market
    context = {'all_products': Product.objects.all()}
    if request.method == 'POST':
        prod = ProductForm(request.POST, request.FILES)
        if prod.is_valid():
            new_product = prod.save(commit=False)
            new_product.owner = request.user
            new_product.save()
            return HttpResponseRedirect(reverse('my_products'))
        context['prod'] = prod
    return render(request, 'products/add_product.html', context)
