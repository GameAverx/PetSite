from django.db import models

class Dishes(models.Model):
    name = models.CharField(max_length=30, db_index=True)

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=1)

    # avatar = models.ImageField(upload_to='static/', blank=True, null=True)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name





















# Create your models here.
