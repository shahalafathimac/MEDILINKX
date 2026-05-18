from django.db import models
from apps.accounts.models import User

# Create your models here.

class Medicine(models.Model):

    supplier = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medicines'
    )

    name = models.CharField(max_length=255)

    description = models.TextField()

    batch_number = models.CharField(max_length=100)

    expiry_date = models.DateField()

    stock_quantity = models.PositiveIntegerField()

    # LOW STOCK ALERT LIMIT
    low_stock_threshold = models.PositiveIntegerField(
        default=10
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    medicine_image = models.ImageField(
        upload_to='medicines/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
