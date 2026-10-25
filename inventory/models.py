
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    image_filename = models.CharField(
    max_length=100,
    blank=True,
    default="pen.svg"
)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.customer_name
    
