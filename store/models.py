from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products/')
    stock=models.IntegerField(default=0)

    def __str__(self):
        return self.name
class Order(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        full_name = models.CharField(max_length=100)
        email = models.EmailField()
        phone = models.CharField(max_length=15)
        address = models.TextField()
        city = models.CharField(max_length=100)
        pincode = models.CharField(max_length=10, default='000000')
        total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
        created_at = models.DateTimeField(auto_now_add=True,null=True)
        def __str__(self):
             return self.full_name

# Create your models here.
