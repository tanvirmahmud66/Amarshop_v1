from django.db import models
from app.models import User, Customer, Product

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)
    