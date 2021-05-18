from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from . import forms
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import channels_redis
from shop.models import Transaction

from django.shortcuts import redirect

# Create your views here.

def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                user=User.objects.create_user(
                    form.cleaned_data['username'],
                    password = form.cleaned_data['password'])
                return HttpResponseRedirect(reverse('acc_login'))
            except IntegrityError:
                form.add_error('username','Username is taken')

        context['form'] = form
    return render(request,'account/signup.html',context)

def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('homepage'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'account/login.html', context)

def do_logout(request):
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})
      
    logout(request)
    return HttpResponseRedirect(reverse('pre_login_home'))

@login_required
def orderhist(request):
    # get all the transaction of the current user
    t = Transaction.objects.filter(user = request.user).all()
    context = {'transactions': t}
    return render(request, 'account/orderhist.html', context)

@login_required
def myproducts(request):
    context = {}
    return render(request, 'account/myproducts.html', context)

@login_required
def myacc(request):
    context = {}
    return render(request, 'account/myacc.html', context)
