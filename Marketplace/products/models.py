from django.db import models
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    # return 'user-' + str(instance.owner.id) + '/' + filename
    return 'user-' + str(instance.owner.id) + '/' + filename


# Create your models here.
class Product(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=150, default='null')
    description = models.CharField(max_length=1000, default='null')
    price = models.DecimalField(max_digits = 7, decimal_places=2)
    # inventory_count = models.CharField(max_length=150, default='null')
    inventory_count = models.DecimalField(max_digits = 5, decimal_places=0)
    image = models.FileField(upload_to=get_upload_path)


    def __str__(self):
        return self.name