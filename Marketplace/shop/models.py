from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
# Individual order item class that represents the products in the cart
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits = 5, decimal_places=0, default=0)

#The Cart that contains all the order items
#Only one cart per user, we delete the cart once the transaction is completed
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    # date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_price(self):
        return sum([i.item.price * i.quantity for i in self.items.all()])

#The Transaction
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    items = models.ManyToManyField(OrderItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.id

    def get_trans_items(self):
        return self.items.all()
