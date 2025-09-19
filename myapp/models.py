from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('others', 'Others'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="General")  # new field
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, default="Unknown")
    # Add "seller" with a different related_name
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_products")  # make sure this exists


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
