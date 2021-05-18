# chat/urls.py
from django.urls import path
# from . import views
import chat.views

urlpatterns = [
    path('', chat.views.index, name='index'),
    path('<str:room_name>/', chat.views.room, name='room'),
]